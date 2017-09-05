# -*- coding: utf-8 -*-
import ROOT
#ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;") #to suppress the output of warnings
#ROOT.gStyle.SetOptStat(0)
from DataFormats.FWLite import Events, Handle
from array import array
import sys
import os


def make_tree(channel):

  datafile = '/storage/7/sfontana/1A8F8A3E-AD24-E711-99B2-0CC47A4D767A.root'
  
  if os.path.exists(datafile):
    events = Events (datafile) #data file downloaded from DAS https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FWLLJJ_WToLNu_EWK_aQGC-FM_ScanUpdate_TuneCUETP8M1_13TeV_madgraph-madspin-pythia8%2FRunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1%2FMINIAODSIM'
    #if you choose another data file the variable sumw (= number of events in the data file) has to be changed!!!
  else:
      print "Data file do not exist!"
      sys.exit()
      
  handle  = Handle ('LHEEventProduct')
  label = ("externalLHEProducer")

  handle_jet = Handle('std::vector<reco::GenJet>')
  label_jet = ('slimmedGenJets')

  #c = ROOT.TCanvas('c','c',1000,800)
  full_diboson = ROOT.TH1F('full_diboson','full_diboson',8,100,2000) #signal histogram with 8 bins


  scale_variations = ['muR1.0_muF2.0','muR1.0_muF0.5','muR2.0_muF1.0','muR2.0_muF2.0','muR0.5_muF1.0','muR0.5_muF0.5'] #needed to calculate the scale uncertainty for the signal
   
  hists = []

  for scale_variation in scale_variations: 
	hists.append(ROOT.TH1F("hist_{0}".format(scale_variation),"hist_{0}".format(scale_variation),8,100,2000)) #Initialize uncertainty histograms

  bins_upperlimit = [0]*8
  bins_lowerlimit = [10000000000000]*8
  full_hist_upperlimit = ROOT.TH1F("full_hist_upperlimit","full_hist_upperlimit",8,100,2000) #upper histogram of the error band
  full_hist_lowerlimit = ROOT.TH1F("full_hist_lowerlimit","full_hist_lowerlimit",8,100,2000) #lower histogram of the error band

  masslist = [] #will be filled with the WZmass (M_{3l + MET})
  weightlist = [] #will be filled with the weights
  #aQGC grid points, the last point has to be the central value
  fm0list1 = [0,-8,-4,-16,8,4, 0, 0,  0, 0,0,0,-8,-8, -8,-8,-8,-8,-4,-4, -4,-4,-4,-4,-16,-16,-16,-16,-16,-16,16,16, 16,16,16,16, 4, 4,  4, 4,4,4, 8, 8,  8, 8,8,8,16]
  fm1list1 = [0, 0, 0,  0,0,0,-8,-4,-16,16,4,8,-8,-4,-16,16, 4, 8,-8,-4,-16,16, 4, 8, -8, -4,-16, 16,  4,  8,-8,-4,-16,16, 4, 8,-8,-4,-16,16,4,8,-8,-4,-16,16,4,8,0]

  def multiply_list(x): return x * 10**(-12)

  fm0list = list(map(multiply_list,fm0list1))
  fm1list = list(map(multiply_list,fm1list1))

  eventnr = 0

  channellist = [] #used to select the choosen final state

  if (channel == 'eee'):
    channellist = [11, 11, 11, 12]
  elif (channel == 'eem'):
    channellist = [11, 11, 13, 14]
  elif (channel == 'mme'):
    channellist = [11, 12, 13, 13]
  elif (channel == 'mmm'):
    channellist = [13, 13, 13, 14]
    

  rfile = ROOT.TFile.Open("ch_{0}_fm.root".format(channel),"RECREATE") #outputfile of the script, needed for python buildWorkspace_AC.py
  tree = ROOT.TTree('tree','outputtree') #outputtree

  #setup the branches of the outputtree
  mass = array('f',[0])
  tree.Branch('WZ_mass',mass,'WZ_mass/F')

  weight = array('f',[0])
  tree.Branch('weight',weight,'weight/F')

  fm0_grid = array('f',[0])
  tree.Branch('fm0_grid',fm0_grid,'fm0_grid/F')

  fm1_grid = array('f',[0])
  tree.Branch('fm1_grid',fm1_grid,'fm1_grid/F')

  for event in events: 

	if(eventnr%5000==0): print "Event ", eventnr

	eventnr = eventnr + 1
	
	event.getByLabel (label, handle)
	
	lhe = handle.product()
	hepeup = lhe.hepeup()
	
	event.getByLabel (label_jet, handle_jet)
	
	lhe_jets = handle_jet.product()

	weights = lhe.weights()  
	
	
	jets = []
	leptons = []
	
	bjets = False #needed for the bjet veto
	
	for p in range(hepeup.NUP):
	  if (11 <= abs(hepeup.IDUP[p]) <= 14):
	    leptons.append(abs(hepeup.IDUP[p])) #create lepton list to recognize the final state
          if (abs(hepeup.IDUP[p]) == 5): #for b jet veto
              q_pup = hepeup.PUP[p]
              lvec = ROOT.TLorentzVector(q_pup[0],q_pup[1],q_pup[2],q_pup[3])
              if(lvec.Pt() > 0): #pt > 0 to ignore b jets in the initial state
                bjets = True
              
        if(bjets == True): continue #if there is a b jet jump to the next event
	    
	leptons.sort() 
	
	if (leptons != channellist): continue #compare leptonlist with wanted final state	
	
	for jet in lhe_jets:
	  if (jet.polarP4().Pt() > 30 and abs(jet.polarP4().Eta()) < 4.7): jets.append(jet) #create jetlist
	
	if (len(jets) < 2): continue #skip event if there are less than 2 jets
        #choose jet with highest pt as leading jet and jet with second highest pt as subleading jet
	leading_jet = jets[0].polarP4()
	leading_jetpt = 0
	leading_jetpt_nr = -1000
	for jetnr in range(len(jets)):
	  jetpt = jets[jetnr].polarP4().Pt()
	  if (jetpt > leading_jetpt): 
	    leading_jet = jets[jetnr].polarP4()
	    leading_jetpt = jetpt
	    leading_jetpt_nr = jetnr
	    
	subleading_jet = jets[0].polarP4()
	subleading_jetpt = 0
	subleading_jetpt_nr = -1000
	for jetnr in range(len(jets)):
	  jetpt = jets[jetnr].polarP4().Pt()
	  if ((jetpt > subleading_jetpt) and (jetnr != leading_jetpt_nr)): 
	    subleading_jet = jets[jetnr].polarP4()
	    subleading_jetpt = jetpt
	    subleading_jetpt_nr = jetnr 


	if ((leading_jet + subleading_jet).M() <= 400): continue  #check if mjj > 400 GeV
	if (abs(leading_jet.Eta() - subleading_jet.Eta()) <= 2.5):continue #check if Delta eta_jj is > 2.5

	nw = 0
	nz = 0
	z_lep_zaehler = 0
	
	wz = ROOT.TLorentzVector(0.,0.,0.,0.)
	wvector = ROOT.TLorentzVector(0,0,0,0)
	zvector = ROOT.TLorentzVector(0,0,0,0)
	lepvector = ROOT.TLorentzVector(0,0,0,0)
	zlepvector = ROOT.TLorentzVector(0,0,0,0)
	lep1vector = ROOT.TLorentzVector(0,0,0,0)
	lep2vector = ROOT.TLorentzVector(0,0,0,0)
	metvector = ROOT.TLorentzVector(0,0,0,0)
	
	for j in xrange(hepeup.NUP):
	  
	  if (abs(hepeup.IDUP[j]) == 16): continue #skip events with tau leptons
	  
	  if(abs(hepeup.IDUP[j]) == 12 or abs(hepeup.IDUP[j]) == 14):#if neutrino
	    pup_met = hepeup.PUP[j]
	    metvector = ROOT.TLorentzVector(pup_met[0],pup_met[1],pup_met[2],pup_met[3])
	    if(metvector.Et() <= 30): continue #check if MET > 30 GeV
	  
	  if (abs(hepeup.IDUP[j]) == 11 or abs(hepeup.IDUP[j]) == 13): #if electron or muon
	    if(abs(hepeup.IDUP[hepeup.MOTHUP[j].second - 1]) == 24): #if electron or muon comes from the W boson, the "-1" is because there is an offset in the indizes
	      pup_lep = hepeup.PUP[j]
	      lepvector = ROOT.TLorentzVector(pup_lep[0],pup_lep[1],pup_lep[2],pup_lep[3])
	      if( lepvector.Pt() <= 20): continue  #check if W lepton pt is > 20 GeV
	      nw = nw +1
	      pup_w = hepeup.PUP[hepeup.MOTHUP[j].second - 1]
	      wvector = ROOT.TLorentzVector(pup_w[0],pup_w[1],pup_w[2],pup_w[3])	

	    else: #assumme other charged leptons come from the Z boson
	      z_lep_zaehler = z_lep_zaehler + 1
	      pup_lep = hepeup.PUP[j]
	      zlepvector = ROOT.TLorentzVector(pup_lep[0],pup_lep[1],pup_lep[2],pup_lep[3])
	      if (z_lep_zaehler == 1):
		lep1_pt = zlepvector.Pt() 
		lep1vector = zlepvector 
	      elif (z_lep_zaehler == 2):	     
		lep2_pt = zlepvector.Pt()
		lep2vector = zlepvector	

                #lepton with higher pt should have pt > 25 GeV, the lepton with the smaller pt should have pt > 15 GeV
		if (lep1_pt > lep2_pt):
		  if (lep1_pt <= 25): continue
		  if (lep2_pt <= 15): continue
		elif (lep1_pt < lep2_pt):
		  if (lep2_pt <= 25): continue
		  if (lep1_pt <= 15): continue
		if ((lep1vector + lep2vector).M() <= 76.1876 or (lep1vector + lep2vector).M() >= 106.1876): continue #check if Z mass is in the +/- 15 GeV Z window
		nz = nz + 1
		pup_z = hepeup.PUP[hepeup.MOTHUP[j].second - 1]  
		zvector = ROOT.TLorentzVector(pup_z[0],pup_z[1],pup_z[2],pup_z[3])
		
	  if ((lepvector + lep1vector + lep2vector).M() <= 100): continue   #check if m_3l > 100 GeV
	
			      
	if ((nw == 1) and (nz == 1)):
	  wz = wvector + zvector	
	  weights = lhe.weights()	
	  lumi = 35.9 #fb^-1
	  xsec = 21.16 #fb^-1
	  sumw = 55106 #= number of events in the sample

	  mass[0] = wz.M()   #fill WZ mass in the outputtree
	  for i in xrange(len(fm0list)):
            #fill weights in the outputtree
            if( i < (len(fm0list) - 1)):
		    if (channel == 'eee'):
		      weight[0] = weights[446 + i].wgt/weights[0].wgt * lumi * xsec / sumw
		    elif (channel == 'eem'):
		      weight[0] = weights[446 + i].wgt/weights[0].wgt * lumi * xsec / sumw  
		    elif (channel == 'mme'):
		      weight[0] = weights[446 + i].wgt/weights[0].wgt * lumi * xsec / sumw
		    elif (channel == 'mmm'):
		      weight[0] = weights[446 + i].wgt/weights[0].wgt * lumi * xsec / sumw 
            else: #fill in the weight of the central point
                    if (channel == 'eee'):
	              weight[0] = weights[0].wgt/weights[0].wgt* lumi * xsec / sumw 
	            elif (channel == 'eem'):
	              weight[0] = weights[0].wgt/weights[0].wgt  * lumi * xsec / sumw  
	            elif (channel == 'mme'):
	              weight[0] = weights[0].wgt/weights[0].wgt* lumi * xsec / sumw 
	            elif (channel == 'mmm'):
	              weight[0] = weights[0].wgt/weights[0].wgt* lumi * xsec / sumw 
	    fm0_grid[0] = fm0list[i] #fill aQGC grid points in the outputtree
	    fm1_grid[0] = fm1list[i]
	    tree.Fill()
	  full_diboson.Fill(wz.M(),weights[446].wgt/weights[0].wgt * lumi * xsec / sumw )#fill signal histogram 
	
          histnr = 0
	  for scalenr in [1,2,3,4,6,8]:
		hists[histnr].Fill(wz.M(),weights[scalenr].wgt/weights[0].wgt * weights[446].wgt/weights[0].wgt *lumi*xsec/sumw) #fill varied signal histograms
                histnr = histnr + 1
        else: #if not exactly one  W boson and one Z boson is found
            continue
#end of event loop---------------------------------------------------------------------------------------------------------


  full_diboson.AddBinContent(8,full_diboson.GetBinContent(9)) #add the overflow to the last bin
  for histnr in range(len(hists)):
        hists[histnr].AddBinContent(8, hists[histnr].GetBinContent(9)) #add the overflow to the last bin
  	for bin in range(1,9): #build envelope of the varied histograms
		        if (hists[histnr].GetBinContent(bin) > bins_upperlimit[bin - 1]):                     
				bins_upperlimit[bin - 1] = hists[histnr].GetBinContent(bin) 
	   		if (hists[histnr].GetBinContent(bin) < bins_lowerlimit[bin - 1]):
				bins_lowerlimit[bin - 1] = hists[histnr].GetBinContent(bin)		  

  for bin in range(1,9):
	full_hist_upperlimit.SetBinContent(bin,bins_upperlimit[bin-1])
	full_hist_lowerlimit.SetBinContent(bin,bins_lowerlimit[bin-1])

#only needed if you want to plot the signal histogram plus the scale uncertainty
  #c.cd() 
  #c.SetLogy();
  #hists[0].SetMaximum(10)
  #hists[0].Draw()
  #for scalenr in range(1,len(scale_variations)):   
	#hists[scalenr].Draw("same")

  #full_hist_upperlimit.SetLineColor(ROOT.kRed)
  #full_hist_upperlimit.SetLineStyle(2)
  #full_hist_upperlimit.SetLineWidth(2)
  #full_hist_lowerlimit.SetLineColor(ROOT.kRed)
  #full_hist_lowerlimit.SetLineStyle(2)
  #full_hist_lowerlimit.SetLineWidth(2)
  #full_hist_upperlimit.Draw("same")
  #full_hist_lowerlimit.Draw("same") 
  #full_diboson.SetLineColor(ROOT.kOrange)
  #full_diboson.SetLineStyle(2)
  #full_diboson.SetLineWidth(2)
  #full_diboson.Draw("same")
   

  #c.SaveAs("sig_scale_variation_{0}.png".format(channel))

  rfile.Write()
  rfile.Close()

  for binnr in range(1,10): #when the loop goes until 9 the 8th bin is not written (I do not know why)
        rootfile = ROOT.TFile('../data/anomalousCoupling/{0}_bin{1}.root'.format(channel,binnr),'UPDATE') #write signal histogram plus uncertainty histograms in the output file
        hist_upperlimit = ROOT.TH1F('hist_upperlimit','hist_upperlimit',1,full_hist_upperlimit.GetXaxis().GetBinLowEdge(binnr),full_hist_upperlimit.GetXaxis().GetBinUpEdge(binnr))
        hist_upperlimit.SetBinContent(1,full_hist_upperlimit.GetBinContent(binnr))
        hist_lowerlimit = ROOT.TH1F('hist_lowerlimit','hist_lowerlimit',1,full_hist_lowerlimit.GetXaxis().GetBinLowEdge(binnr),full_hist_lowerlimit.GetXaxis().GetBinUpEdge(binnr))
        hist_lowerlimit.SetBinContent(1,full_hist_lowerlimit.GetBinContent(binnr))
        hist_upperlimit.SetName("sig_scale_variationUp")
        hist_lowerlimit.SetName("sig_scale_variationDown")
        hist_upperlimit.Write('',ROOT.TObject.kOverwrite)
        hist_lowerlimit.Write('',ROOT.TObject.kOverwrite) 
  for binnr in range(1,9):
        rootfile_bins = ROOT.TFile('../data/anomalousCoupling/{0}_bin{1}.root'.format(channel,binnr),'UPDATE') 
        diboson = ROOT.TH1F('diboson','diboson',1,full_diboson.GetXaxis().GetBinLowEdge(binnr),full_diboson.GetXaxis().GetBinUpEdge(binnr))
        diboson.SetBinContent(1,full_diboson.GetBinContent(binnr))
        diboson.Write('',ROOT.TObject.kOverwrite)
  rootfile.Close()
  rootfile_bins.Close()
  
  print "Number of events in the sample: ",eventnr

  print 'created {0}.root'.format(channel) 

  #--------------------------------------------end of function make_tree-----------------------------------------------


make_tree('eee')
make_tree('eem')
make_tree('mme')
make_tree('mmm')


