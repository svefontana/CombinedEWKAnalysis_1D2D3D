# -*- coding: utf-8 -*-
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")
from DataFormats.FWLite import Events, Handle
from array import array
from math import floor

import os
import os.path
import sys

def make_tree(channel):

  z = 0

  events = Events ('/storage/7/sfontana/1802E3A1-CF1B-E711-965A-0025905A60D2.root')
  handle  = Handle ('LHEEventProduct')
  label = ("externalLHEProducer")

  handle_jet = Handle('std::vector<reco::GenJet>')
  label_jet = ('slimmedGenJets')

  c = ROOT.TCanvas('c','c',1200,1100)
  full_diboson = ROOT.TH1F('full_diboson','full_diboson',8,100,2000) #for data/bkg tree
  #histo_ft2_0_first = ROOT.TH1F("histo_ft2_0",' histo_ft2_0',7,100,800)
  #histo_ft0_4_first = ROOT.TH1F("histo_ft0_4",' histo_ft0_4',7,100,800)
  #histo_ft0_m16_first = ROOT.TH1F("histo_ft0_m16",' histo_ft0_m16',7,100,800)
  #histo_ft0_8_first = ROOT.TH1F("histo_ft0_8",' histo_ft0_8',7,100,800)
  #histo_ft0_m8_first = ROOT.TH1F("histo_ft0_m8",' histo_ft0_m8',7,100,800)
  #histo_ft0_16_first = ROOT.TH1F("histo_ft0_16",' histo_ft0_16',7,100,800)
  #histo_ft0_m4_first = ROOT.TH1F("histo_ft0_m4",' histo_ft0_m4',7,100,800)
  
  #legend = ROOT.TLegend(0.35,0.65,0.5,0.89)
  #legend.SetFillColor(0) 
  #legend.SetBorderSize(0) 
  #legend.SetTextSize(0.025) 
  
  scale_variations = ['muR1.0_muF2.0','muR1.0_muF0.5','muR2.0_muF1.0','muR2.0_muF2.0','muR0.5_muF1.0','muR0.5_muF0.5']
   
  hists = []

  for scale_variation in scale_variations: 
	hists.append(ROOT.TH1F("hist_{0}".format(scale_variation),"hist_{0}".format(scale_variation),8,100,2000))

  bins_upperlimit = [0]*8
  bins_lowerlimit = [10000000000000]*8
  full_hist_upperlimit = ROOT.TH1F("full_hist_upperlimit","full_hist_upperlimit",8,100,2000)
  full_hist_lowerlimit = ROOT.TH1F("full_hist_lowerlimit","full_hist_lowerlimit",8,100,2000)


  masslist = []
  weightlist = []
  ft0list1 = [0,-0.5,-1,-1.5,-2,1.5,0.5,2,   0, 0,   0, 0,0,  0,0,  0,0,  0, 0, 0,0,0,0,0,1]
  ft1list1 = [0,   0, 0,   0, 0,  0,  0,0,-0.5,-1,-1.5,-2,1,1.5,2,0.5,0 , 0 ,0 ,0,0,0,0,0,0]
  ft2list1 = [0,   0, 0,   0, 0,  0,  0,0,   0, 0,   0, 0,0,  0,0,  0,-1,-2,-3,-6,6,3,2,1,0]

  def multiply_list(x): return x * 10**(-12)

  ft0list = list(map(multiply_list,ft0list1))
  ft1list = list(map(multiply_list,ft1list1))
  ft2list = list(map(multiply_list,ft2list1))

  eventnr = 0

  channellist = []

  if (channel == 'eee'):
    channellist = [11, 11, 11, 12]
  elif (channel == 'eem'):
    channellist = [11, 11, 13, 14]
  elif (channel == 'mme'):
    channellist = [11, 12, 13, 13]
  elif (channel == 'mmm'):
    channellist = [13, 13, 13, 14]
    

  rfile = ROOT.TFile.Open("ch_{0}_ft.root".format(channel),"RECREATE")
  tree = ROOT.TTree('tree','outputtree')

  mass = array('f',[0])
  tree.Branch('WZ_mass',mass,'WZ_mass/F')

  weight = array('f',[0])
  tree.Branch('weight',weight,'weight/F')

  ft0_grid = array('f',[0])
  tree.Branch('ft0_grid',ft0_grid,'ft0_grid/F')

  ft1_grid = array('f',[0])
  tree.Branch('ft1_grid',ft1_grid,'ft1_grid/F')
  
  ft2_grid = array('f',[0])
  tree.Branch('ft2_grid',ft2_grid,'ft2_grid/F')

  for event in events: 
      
        z = z + 1

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
	
	for p in range(hepeup.NUP):
	  if (11 <= abs(hepeup.IDUP[p]) <= 14):
	    leptons.append(abs(hepeup.IDUP[p]))
	    
	leptons.sort()
	
	if (leptons != channellist): continue      

	
	for jet in lhe_jets:
	  if (jet.polarP4().Pt() > 30 and jet.polarP4().Eta() < 4.7): jets.append(jet)
	
	if (len(jets) < 2): continue
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


	if ((leading_jet + subleading_jet).M() <= 400): continue  
	if (abs(leading_jet.Eta() - subleading_jet.Eta()) <= 2.5):continue

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
	  
	  if (abs(hepeup.IDUP[j]) == 16): continue #skip events with tau
	  
	  if(abs(hepeup.IDUP[j]) == 12 or abs(hepeup.IDUP[j]) == 14):#Neutrinos
	    pup_met = hepeup.PUP[j]
	    metvector = ROOT.TLorentzVector(pup_met[0],pup_met[1],pup_met[2],pup_met[3])
	    if(metvector.Et() <= 30): continue
	  
	  if (abs(hepeup.IDUP[j]) == 11 or abs(hepeup.IDUP[j]) == 13): #e oder mu
	    if(abs(hepeup.IDUP[hepeup.MOTHUP[j].second - 1]) == 24): #e oder mu von W, Offset in Indizes
	      pup_lep = hepeup.PUP[j]
	      lepvector = ROOT.TLorentzVector(pup_lep[0],pup_lep[1],pup_lep[2],pup_lep[3])
	      if( lepvector.Pt() <= 20): continue  
	      nw = nw +1
	      pup_w = hepeup.PUP[hepeup.MOTHUP[j].second - 1]
	      wvector = ROOT.TLorentzVector(pup_w[0],pup_w[1],pup_w[2],pup_w[3])	

	    else: #assumme other charged leptons come from Z
	      z_lep_zaehler = z_lep_zaehler + 1
	      pup_lep = hepeup.PUP[j]
	      zlepvector = ROOT.TLorentzVector(pup_lep[0],pup_lep[1],pup_lep[2],pup_lep[3])
	      if (z_lep_zaehler == 1):
		lep1_pt = zlepvector.Pt() 
		lep1vector = zlepvector 
	      elif (z_lep_zaehler == 2):	     
		lep2_pt = zlepvector.Pt()
		lep2vector = zlepvector	

		if (lep1_pt > lep2_pt):
		  if (lep1_pt <= 25): continue
		  if (lep2_pt <= 15): continue
		elif (lep1_pt < lep2_pt):
		  if (lep2_pt <= 25): continue
		  if (lep1_pt <= 15): continue
		if ((lep1vector + lep2vector).M() <= 76.1876 or (lep1vector + lep2vector).M() >= 106.1876): continue
		nz = nz + 1
		pup_z = hepeup.PUP[hepeup.MOTHUP[j].second - 1]  
		zvector = ROOT.TLorentzVector(pup_z[0],pup_z[1],pup_z[2],pup_z[3])
		
	  if ((lepvector + lep1vector + lep2vector).M() <= 100): continue	
			      
	if ((nw == 1) and (nz == 1)):
	  wz = wvector + zvector
	  
	  weights = lhe.weights()
	  lumi = 35.9 #fb^-1
	  xsec = 16.23 
	  sumw = 55913
	
	  mass[0] = wz.M()
	  for i in xrange(len(ft0list)):
            if( i < (len(ft0list) - 1)):
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
	    ft0_grid[0] = ft0list[i]
	    ft1_grid[0] = ft1list[i]
	    ft2_grid[0] = ft2list[i]
	    tree.Fill()
	  full_diboson.Fill(wz.M(),weights[446].wgt/weights[0].wgt * lumi * xsec / sumw)#WQ *Lumi/Summe ueber alle SM Gewichte ohne Auswahl auf Gewichte fuer Tree und fuer dibosonhisto

	  histnr = 0
	  for scalenr in [1,2,3,4,6,8]:
		hists[histnr].Fill(wz.M(),weights[scalenr].wgt/weights[0].wgt * weights[446].wgt/weights[0].wgt *lumi*xsec/sumw) 
                histnr = histnr + 1   
	    ##ft2 = 0
	    #if(weights[446 + i].id == 'standard_model'):
	      #histo_ft2_0_first.Fill(wz.M(),weights[446 + i].wgt)
	    #if(weights[446 + i].id == 'ft0_16__ft1_0__ft2_0'): #ft0 = 16
	      #histo_ft0_16_first.Fill(wz.M(),weights[446 + i].wgt)
	    #if(weights[446 + i].id == 'ft0_m16__ft1_0__ft2_0'): #ft0 = -16
	      #histo_ft0_m16_first.Fill(wz.M(),weights[446 + i].wgt)
	    #if(weights[446 + i].id == 'ft0_m8__ft1_0__ft2_0'): #ft0 = -8
	      #histo_ft0_m8_first.Fill(wz.M(),weights[446 + i].wgt)
	    #if(weights[446 + i].id == 'ft0_m4__ft1_0__ft2_0'): #ft0 = -4
	      #histo_ft0_m4_first.Fill(wz.M(),weights[446 + i].wgt)
	    ##if(weights[446 + i].id == 'ft0_16__ft1_0__ft2_0'): #ft0 = 16
	      ##histo_ft0_16_first.Fill(wz.M(),weights[446 + i].wgt)
	    #if(weights[446 + i].id == 'ft0_4__ft1_0__ft2_0'): #ft0 = 4
	      #histo_ft0_4_first.Fill(wz.M(),weights[446 + i].wgt)
	      
	
	else:
	  #print "didn't find wz"
	  continue
	
  #histo_ft2_0 = ROOT.TH1F("histo_ft2_0",' histo_ft2_0',8,100,900)
  #histo_ft0_4 = ROOT.TH1F("histo_ft0_4",' histo_ft0_4',8,100,900)
  #histo_ft0_m16 = ROOT.TH1F("histo_ft0_m16",' histo_ft0_m16',8,100,900)
  ##histo_ft0_8 = ROOT.TH1F("histo_ft0_8",' histo_ft0_8',8,100,900)
  #histo_ft0_m8 = ROOT.TH1F("histo_ft0_m8",' histo_ft0_m8',8,100,900)
  #histo_ft0_16 = ROOT.TH1F("histo_ft0_16",' histo_ft0_16',8,100,900)
  #histo_ft0_m4 = ROOT.TH1F("histo_ft0_m4",' histo_ft0_m4',8,100,900)


  #for bin in range(1,9):
    #histo_ft2_0.SetBinContent(bin,histo_ft2_0_first.GetBinContent(bin))
    #histo_ft0_16.SetBinContent(bin,histo_ft0_16_first.GetBinContent(bin))
    #histo_ft0_m4.SetBinContent(bin,histo_ft0_m4_first.GetBinContent(bin))
    ##histo_ft0_8.SetBinContent(bin,histo_ft0_8_first.GetBinContent(bin))
    #histo_ft0_m8.SetBinContent(bin,histo_ft0_m8_first.GetBinContent(bin))
    #histo_ft0_4.SetBinContent(bin,histo_ft0_4_first.GetBinContent(bin))
    #histo_ft0_m16.SetBinContent(bin,histo_ft0_m16_first.GetBinContent(bin))

  #c.cd()
  #histo_ft0_16.SetLineColor(ROOT.kRed)
  #histo_ft0_m4.SetLineColor(ROOT.kYellow)
  ##histo_ft0_8.SetLineColor(ROOT.kOrange)
  #histo_ft0_m8.SetLineColor(ROOT.kGreen)
  #histo_ft0_4.SetLineColor(ROOT.kViolet)
  #histo_ft0_m16.SetLineColor(ROOT.kBlack)
  
  #histo_ft0_m16.SetLineWidth(2)
  #histo_ft0_m4.SetLineWidth(2)
  #histo_ft0_m8.SetLineWidth(2)
  #histo_ft0_4.SetLineWidth(2)
  #histo_ft0_m16.SetLineWidth(2)
  
  #legend.AddEntry(histo_ft2_0,"standard model")
  #legend.AddEntry(histo_ft0_16,"ft0 = 16")
  #legend.AddEntry(histo_ft0_m4,"ft0 = -4")
  ##legend.AddEntry(histo_ft0_8,"ft0 = 8")
  #legend.AddEntry(histo_ft0_m8,"ft0 = -8")
  #legend.AddEntry(histo_ft0_4,"ft0 = 4")
  #legend.AddEntry(histo_ft0_m16,"ft0 = -16")
 
  ##histo_ft0_16.SetMaximum(0.07)


  
  #histo_ft2_0.Draw("histo")
  #histo_ft0_16.Draw("same histo")
  #histo_ft0_m4.Draw("same histo")
  ##histo_ft0_8.Draw("same histo")
  #histo_ft0_m8.Draw("same histo")
  #histo_ft0_4.Draw("same histo")
  #histo_ft0_m16.Draw("same histo")   
  #legend.Draw("same")

  
  #c.SaveAs("{0}.png".format(channel))
  #end of event loop---------------------------------------------------------------------------------------------------------


  full_diboson.AddBinContent(8,full_diboson.GetBinContent(9)) 
  for histnr in range(len(hists)):
        hists[histnr].AddBinContent(8, hists[histnr].GetBinContent(9))
  	for bin in range(1,9):
		        if (hists[histnr].GetBinContent(bin) > bins_upperlimit[bin - 1]):                     
				bins_upperlimit[bin - 1] = hists[histnr].GetBinContent(bin) 
	   		if (hists[histnr].GetBinContent(bin) < bins_lowerlimit[bin - 1]):
				bins_lowerlimit[bin - 1] = hists[histnr].GetBinContent(bin)		  

  for bin in range(1,9):
	full_hist_upperlimit.SetBinContent(bin,bins_upperlimit[bin-1])
	full_hist_lowerlimit.SetBinContent(bin,bins_lowerlimit[bin-1])
	
  rfile.Write()
  rfile.Close()

  for binnr in range(1,10): #when the loop goes until 9 the 8th bin is not written
        rootfile = ROOT.TFile('/home/sfontana/CMSSW_7_1_5/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/{0}_bin{1}.root'.format(channel,binnr),'UPDATE') #for data/bkg tree
        hist_upperlimit = ROOT.TH1F('hist_upperlimit','hist_upperlimit',1,full_hist_upperlimit.GetXaxis().GetBinLowEdge(binnr),full_hist_upperlimit.GetXaxis().GetBinUpEdge(binnr))
        hist_upperlimit.SetBinContent(1,full_hist_upperlimit.GetBinContent(binnr))
        hist_lowerlimit = ROOT.TH1F('hist_lowerlimit','hist_lowerlimit',1,full_hist_lowerlimit.GetXaxis().GetBinLowEdge(binnr),full_hist_lowerlimit.GetXaxis().GetBinUpEdge(binnr))
        hist_lowerlimit.SetBinContent(1,full_hist_lowerlimit.GetBinContent(binnr))
        hist_upperlimit.SetName("sig_scale_variationUp")
        hist_lowerlimit.SetName("sig_scale_variationDown")
        hist_upperlimit.Write('',ROOT.TObject.kOverwrite)
        hist_lowerlimit.Write('',ROOT.TObject.kOverwrite) 
  for binnr in range(1,9):
        rootfile_bins = ROOT.TFile('/home/sfontana/CMSSW_7_1_5/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/{0}_bin{1}.root'.format(channel,binnr),'UPDATE') 
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


