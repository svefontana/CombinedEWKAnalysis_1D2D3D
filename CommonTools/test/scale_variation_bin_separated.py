# -*- coding: utf-8 -*-
import ROOT
ROOT.gROOT.SetBatch(True)

import os
import os.path
import sys


def create_envelope(channel,binnr): #creates the scale uncertainty band as envelope of the varies histograms
	samples = ['ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8','WZTo3LNu_0Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WZTo3LNu_1Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WZTo3LNu_2Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WZTo3LNu_3Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','ZZTo4L_13TeV_powheg_pythia8','tZq_ll_4f_13TeV-amcatnlo-pythia8','ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8','WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8','WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8','WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8']

        mcfiles = [] # input files for the nominal histogram
	for sample in samples:
    		mcfiles.append(ROOT.TFile('/home/sfontana/CMSSW_7_1_5/src/CombinedEWKAnalysis/CommonTools/test/VBS_cutbased/VBS_cutbased_with_deltaRcut_allhistos/{0}.root'.format(sample),'read'))

	histnr = 0 #chooses correct file
	hists = []

	c = ROOT.TCanvas('c','c',1000,800)

	infiles = [] # input files for the histograms with varied pdf weights

	mc_bkg = ROOT.TH1F("hist","hist",1,mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF0.5/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinLowEdge(binnr),mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF0.5/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinUpEdge(binnr))

	scale_variations = ['genWeight_muR1.0_muF0.5','genWeight_muR1.0_muF2.0','genWeight_muR2.0_muF1.0','genWeight_muR2.0_muF2.0','genWeight_muR0.5_muF1.0','genWeight_muR0.5_muF0.5']

	hists = []	

	for scale_variation in scale_variations: 
		hists.append(ROOT.TH1F("hist_{0}".format(scale_variation),"hist_{0}".format(scale_variation),1,mcfiles[0].Get('PPP/signal_region/{1}/{0}/WZ_mass'.format(channel,scale_variation)).GetXaxis().GetBinLowEdge(binnr),mcfiles[0].Get('PPP/signal_region/{1}/{0}/WZ_mass'.format(channel,scale_variation)).GetXaxis().GetBinUpEdge(binnr)))

	bins_upperlimit = [0]*8
	bins_lowerlimit = [1000]*8
	hist_upperlimit = ROOT.TH1F("hist_upperlimit","hist_upperlimit",1,mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF0.5/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinLowEdge(binnr),mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF0.5/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinUpEdge(binnr))
	hist_lowerlimit = ROOT.TH1F("hist_lowerlimit","hist_lowerlimit",1,mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF0.5/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinLowEdge(binnr),mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF0.5/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinUpEdge(binnr))	


	for scalenr in range(len(scale_variations)):  #creates varied histograms
		for sample in samples:
	  		infiles.append(ROOT.TFile('/home/sfontana/CMSSW_7_1_5/src/CombinedEWKAnalysis/CommonTools/test/VBS_cutbased/VBS_cutbased_with_deltaRcut_allhistos/{0}.root'.format(sample),'read')) 
		for sample in samples:
		  hists[scalenr].AddBinContent(1,infiles[histnr].Get('PPP/signal_region/{1}/{0}/WZ_mass'.format(channel,scale_variations[scalenr])).GetBinContent(binnr))
		  if (binnr == 8):
                    hists[scalenr].AddBinContent(1,infiles[histnr].Get('PPP/signal_region/{1}/{0}/WZ_mass'.format(channel,scale_variations[scalenr])).GetBinContent(9))
		  histnr = histnr + 1    
                #build  envelope
                if (hists[scalenr].GetBinContent(1) > bins_upperlimit[1]):                     
                        bins_upperlimit[1] = hists[scalenr].GetBinContent(1) 
                if (hists[scalenr].GetBinContent(1) < bins_lowerlimit[1]):
                        bins_lowerlimit[1] = hists[scalenr].GetBinContent(1)            


        hist_upperlimit.SetBinContent(1,bins_upperlimit[1])
        hist_lowerlimit.SetBinContent(1,bins_lowerlimit[1])

	c.cd() 
	hists[0].Draw()
	for scalenr in range(1,len(scale_variations)): 
                #hists[scalenr].SetLineColor(ROOT.kRed)
		hists[scalenr].Draw("same")
    
        histnr = 0
        
       	for sample in samples:   #creates nominal histogram               
                  mc_bkg.AddBinContent(1,mcfiles[histnr].Get('PPP/signal_region/genWeight_muR1.0_muF1.0/{0}/WZ_mass'.format(channel)).GetBinContent(binnr))
                  if (binnr == 8):
                    mc_bkg.AddBinContent(1,mcfiles[histnr].Get('PPP/signal_region/genWeight_muR1.0_muF1.0/{0}/WZ_mass'.format(channel)).GetBinContent(9))
                  histnr = histnr + 1
        
#draws histograms to check band
	hist_upperlimit.SetLineColor(ROOT.kRed)
        hist_upperlimit.SetLineStyle(2)
        hist_upperlimit.SetLineWidth(2)
	hist_lowerlimit.SetLineColor(ROOT.kRed)
        hist_lowerlimit.SetLineStyle(2)
        hist_lowerlimit.SetLineWidth(2)
	hist_upperlimit.Draw("same")
	hist_lowerlimit.Draw("same") 
        mc_bkg.SetLineColor(ROOT.kGreen)
        mc_bkg.SetLineStyle(2)
        mc_bkg.SetLineWidth(2)
        mc_bkg.Draw("hist same")

	c.SaveAs("scale_variation_{0}_bin{1}.png".format(channel,binnr))

        #write histograms to file
	rootfile = ROOT.TFile('/home/sfontana/CMSSW_7_1_5/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/{0}_bin{1}.root'.format(channel,binnr),'UPDATE') 
	hist_upperlimit.SetName("scale_variationUp")
	hist_lowerlimit.SetName("scale_variationDown")
        hist_upperlimit.Write('',ROOT.TObject.kOverwrite)
	hist_lowerlimit.Write('',ROOT.TObject.kOverwrite)
        rootfile.Close()
        
#------------------------------------------        
for c in ['eee','eem','mme','mmm']:
    for b in range(1,9):
        create_envelope(c,b)


