#this script creates the nonprompt background, MC background and pseudo data histograms for the nominal case and for the jet/lepton uncertainties, furthermore, a poisson error band for the nominal nonprompt background is created

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;") #suppresses the output of warnings

#this script creates the nonprompt background, MC background and pseudo data histograms for the nominal case and for the jet/lepton uncertainties, furthermore, a scaled poisson error band for the nominal nonprompt background is created

def poisson_shape(hist, direction,binnr): #creates scaled poisson error band (direction = "up"/"down" for up/down histogram) for bin "binnr" of the histogram "hist"
  chisqr = ROOT.TMath.ChisquareQuantile
  staterr = hist.Clone("staterr")
  uncertainty_hist = ROOT.TH1F("uncertainty_hist","uncertainty_hist",staterr.GetNbinsX(),staterr.GetXaxis().GetBinLowEdge(1),staterr.GetXaxis().GetBinUpEdge(8))  
  staterr.Sumw2(ROOT.kTRUE) 
  sumw2 = 0
  for b in range(hist.GetNbinsX()):
    sumw2 = sumw2 + (staterr.GetBinError(b + 1))**2
  sumw  =  staterr.Integral()
  if (sumw2 != 0):
        scalefactor = sumw/sumw2 #taken from https://arxiv.org/abs/1309.1287
  else:
        scalefactor = 1
  staterr.Sumw2(ROOT.kFALSE) 
  staterr.SetBinErrorOption(ROOT.TH1.kPoisson)
  entries = staterr.GetBinContent(binnr)
  err_low = (entries - 0.5 * chisqr(0.1586555, 2. * entries)) * scalefactor 
  err_up =  (0.5 * chisqr(1. - 0.1586555, 2. * (entries + 1)) - entries) * scalefactor
  if (direction == "up"):
      uncertainty_hist.SetBinContent(1,entries + err_up)
  elif (direction == "down"):   
      uncertainty_hist.SetBinContent(1,entries - err_low)
  else:
      print "Unknown direction. Valid directions are up and down."
  return uncertainty_hist

#--------------------------------------------------------------------------------------------------------------------------------------
def make_histos(channel,binnr,uncertainty):#creates the histograms, uncertainty = off (for the nominal case), ElectronEnUp, MuonEnDown..., channel=eee,eem,mme or mmm, binnr = number of the bin in the input histograms
    
    #input histograms
    #nominal histograms are provided as, e.g., PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass
    #up/down histos are provided as, e.g., PPF/signal_region/eee/WZ_mass
    
  if (uncertainty == 'off'):
      weight = '/genWeight_muR1.0_muF1.0/'
  else:
      weight = '/'  
  
  samples = ["DoubleEG","DoubleMuon",'SingleMuon','SingleElectron','MuonEG','ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8','WZTo3LNu_0Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WZTo3LNu_1Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WZTo3LNu_2Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WZTo3LNu_3Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','ZZTo4L_13TeV_powheg_pythia8','tZq_ll_4f_13TeV-amcatnlo-pythia8','ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8','WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8','WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8','WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8']
  fakeRegions = ['PPF','PFP','FPP','PFF','FPF','FFP','FFF']

  #stack = ROOT.THStack()
 # mc_stack = ROOT.THStack()

  infiles = []

  for sample in samples: #create list of input root files
    if (uncertainty == "off"):
    	infiles.append(ROOT.TFile('VBS_cutbased/VBS_cutbased_with_deltaRcut_allhistos/{0}.root'.format(sample),'read'))
    else:
    	infiles.append(ROOT.TFile('VBS_cutbased/VBS_cutbased_{1}_with_deltaRcut/{0}.root'.format(sample,uncertainty),'read'))

  #initialize histograms
  if (uncertainty == "off"):
    #h_nonprompt_complete is needed to scale the poisson error
    h_nonprompt_complete = ROOT.TH1D('h_nonprompt_complete','h_nonprompt_complete',infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetNbinsX(),infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetXmin(),infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetXmax())
    # h_nonprompt = final nonprompt histogram with one bin, bins are separated to calculate the statistical error correctly
    h_nonprompt = ROOT.TH1D('h_nonprompt','h_nonprompt',1,infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetBinLowEdge(binnr),infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetBinUpEdge(binnr))
    # h_nonpromptUp/Down are used as statistical error band for the nonprompt background
    h_nonpromptUp = ROOT.TH1D('h_nonprompt_statsyst_{0}_{1}Up'.format(channel,binnr),'h_nonprompt_statsyst_{0}_{1}Up'.format(channel,binnr),1,infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetBinLowEdge(binnr),infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetBinUpEdge(binnr))
    h_nonpromptDown = ROOT.TH1D('h_nonprompt_statsyst_{0}_{1}Down'.format(channel,binnr),'h_nonprompt_statsyst_{0}_{1}Down'.format(channel,binnr),1,infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetBinLowEdge(binnr),infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetBinUpEdge(binnr))
    mc_bkg = ROOT.TH1D('mc_bkg','mc_bkg',1,infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetBinLowEdge(binnr),infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetBinUpEdge(binnr))
    data_obs = ROOT.TH1F('data_obs','data_obs',1,infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetBinLowEdge(binnr),infiles[0].Get('PPF/signal_region/genWeight_muR1.0_muF1.0/eee/WZ_mass').GetXaxis().GetBinUpEdge(binnr))
  else:   #lepton/jet uncertainties are only calculated for the MC background
    mc_bkg = ROOT.TH1D('mc_bkg_{0}'.format(uncertainty),'mc_bkg_{0}'.format(uncertainty),1,infiles[0].Get('PPF/signal_region/eee/WZ_mass').GetXaxis().GetBinLowEdge(binnr),infiles[0].Get('PPF/signal_region/eee/WZ_mass').GetXaxis().GetBinUpEdge(binnr))


  #output root file
  rootfile = ROOT.TFile('/home/sfontana/CMSSW_7_1_5/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/{0}_bin{1}.root'.format(channel,binnr),'Update')


#--------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------Nonprompt--------------------------------------------------------------------
  if (uncertainty == "off"):
        nonprompt_sumw2 = [0]*9 #to set sumw2 for the nonprompt histogram
        
        for sampleNr in range(0,len(samples)): #add the histograms of all samples and fakeRegions, weights are already applied to the histograms
            for region in fakeRegions:
                h_nonprompt_complete =h_nonprompt_complete + infiles[sampleNr].Get('{0}/signal_region{2}{1}/WZ_mass'.format(region, channel,weight)) 
                for b in range (1,9):
                    nonprompt_sumw2[b] = nonprompt_sumw2[b] +  (infiles[sampleNr].Get('{0}/signal_region{2}{1}/WZ_mass'.format(region,channel,weight)).GetBinError(b))**2
            
        for bin in range(h_nonprompt_complete.GetNbinsX()+1): #set negative background to nearly zero
                if(h_nonprompt_complete.GetBinContent(bin + 1) <= 0):
                        h_nonprompt_complete.SetBinContent(bin + 1,0.01)

        h_nonprompt_complete.AddBinContent(8,h_nonprompt.GetBinContent(9)) #add the overflow to the last bin
        nonprompt_sumw2[8] = nonprompt_sumw2[8] + (infiles[sampleNr].Get('{0}/signal_region{2}{1}/WZ_mass'.format(region,channel,weight)).GetBinError(9))**2
        for b in range (1,9):
            h_nonprompt_complete.SetBinError(b,nonprompt_sumw2[b]) #set sumw2 for the nonprompt histogram        
            
        #poisson error band    
        h_nonpromptUp.SetBinContent(1,poisson_shape(h_nonprompt_complete,"up",binnr).GetBinContent(1))
        h_nonpromptDown.SetBinContent(1,poisson_shape(h_nonprompt_complete,"down",binnr).GetBinContent(1))
        if poisson_shape(h_nonprompt_complete,"down",binnr).GetBinContent(1) <= 0:  h_nonpromptDown.SetBinContent(1,0.001) #set negative down histos to nearly zero, combine do not like bins <= 0
         
        #separate the relevant bin 
        h_nonprompt.SetBinContent(1,h_nonprompt_complete.GetBinContent(binnr))
        h_nonprompt.SetBinError(1,h_nonprompt_complete.GetBinError(binnr))
        
#--------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------MC-------------------------------------------------------------------------

  histnr = 0
  mc_error = 0
  
  #add histograms of the different samples and set the error
    
  for samplenr in range(5,len(samples)):          
         mc_bkg.AddBinContent(1,infiles[samplenr].Get('PPP/signal_region{1}{0}/WZ_mass'.format(channel,weight)).GetBinContent(binnr))
         mc_error = mc_error +  (infiles[samplenr].Get('PPP/signal_region{1}{0}/WZ_mass'.format(channel,weight)).GetBinError(binnr))**2
         if (binnr == 8): #add the overflow to the last bin
            mc_bkg.AddBinContent(1,infiles[samplenr].Get('PPP/signal_region{1}{0}/WZ_mass'.format(channel,weight)).GetBinContent(9))
            mc_error = mc_error +  (infiles[samplenr].Get('PPP/signal_region{1}{0}/WZ_mass'.format(channel,weight)).GetBinError(binnr))**2
         histnr = histnr + 1  
         
  mc_bkg.SetBinError(1,mc_error)    
  
  #-------------------------------------------------------------Pseudo Data---------------------------------------------------------------------

#create pseudo data as poisson distributed around the background distribution
  if (uncertainty == "off"):
        r = ROOT.TRandom()
        
        data_obs.Sumw2()
        bincontent = r.Poisson(h_nonprompt.GetBinContent(1) + mc_bkg.GetBinContent(1))
        data_obs.SetBinContent(1,bincontent)
        data_obs.SetBinError(1,ROOT.TMath.Sqrt(bincontent))
        
        data_obs.Write('',ROOT.TObject.kOverwrite) 

  
  mc_bkg.Write('',ROOT.TObject.kOverwrite)   
  if (uncertainty == "off"):
    h_nonprompt.Write('',ROOT.TObject.kOverwrite)
    h_nonpromptDown.Write('',ROOT.TObject.kOverwrite)
    h_nonpromptUp.Write('',ROOT.TObject.kOverwrite)
  #rootfile.Close() #leads to a segmentation fault
 
#-------------------------end of function------------------------------------------------------
 
channels = ['eee','eem','mme','mmm']
uncertainties = ['off','ElectronEnUp', 'ElectronEnDown','UnclusteredEnUp','UnclusteredEnDown','MuonEnUp', 'MuonEnDown','JetEnUp','JetEnDown']

for channel in channels: 
    for binnr in range(1,9):
        print "-------------------------"
	for uncertainty in uncertainties:
            print uncertainty  
            print "--------------------"
	    make_histos(channel,binnr,uncertainty)









