import ROOT
ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")#suppresses the output of warnings

def correct_uncertaintybands(channel,binnr,uncertainty): #if the nominal histogram is outside the error band the "correct" side of the error band is mirrored to the other side of the nominal histogram

    #the input root file is the output root file of data_bkg_histos_bin_separated.py
    rootfile = ROOT.TFile('/home/sfontana/CMSSW_7_1_5/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/{0}_bin{1}.root'.format(channel,binnr),'Read')  
    nominal = rootfile.Get('mc_bkg').GetBinContent(1)
    up = rootfile.Get('mc_bkg_{0}Up'.format(uncertainty)).GetBinContent(1)
    down = rootfile.Get('mc_bkg_{0}Down'.format(uncertainty)).GetBinContent(1)    
        
    if (down > up): #swaps up/down histograms if needed
        tmp = down
        down = up
        up = tmp
    
    mc_bkg_down = ROOT.TH1D('mc_bkg_{0}Down'.format(uncertainty),'mc_bkg_{0}Down'.format(uncertainty),1,100 + (binnr - 1) * 237.5,100 + binnr * 237.5) #237.5 is the bin width
    mc_bkg_up = ROOT.TH1D('mc_bkg_{0}Up'.format(uncertainty),'mc_bkg_{0}Up'.format(uncertainty),1,100 + (binnr - 1) * 237.5,100 + binnr * 237.5)
    
    
    if (nominal <= down): #new down = mirrored up histogram
        new_down = nominal - (up - nominal)
        if (new_down < 0): new_down = 0.001
        mc_bkg_down.SetBinContent(1,new_down)  
        mc_bkg_up.SetBinContent(1,up) 
    elif (up <= nominal): #new up = mirrored down histogram
        mc_bkg_up.SetBinContent(1,nominal + (nominal - down))
        mc_bkg_down.SetBinContent(1,down)
    else: #everything is okay, histograms stay as they are
        mc_bkg_up.SetBinContent(1,up)
        mc_bkg_down.SetBinContent(1,down)        
    
    outfile = ROOT.TFile('/home/sfontana/CMSSW_7_1_5/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/{0}_bin{1}.root'.format(channel,binnr),'Update') #overwrite input file
    mc_bkg_up.Write('',ROOT.TObject.kOverwrite)
    mc_bkg_down.Write('',ROOT.TObject.kOverwrite)
    
#---------------------------------------------------------------------------------------------
        
for uncertainty in ['JetEn','MuonEn','ElectronEn','UnclusteredEn']:         
    for channel in ['eee','eem','mme','mmm']:
        for binnr in range(1,9):
            print channel,binnr,uncertainty
            correct_uncertaintybands(channel,binnr,uncertainty)