# -*- coding: utf-8 -*-
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")

def create_pdf_uncertainties(channel,binnr):#creates the pdf uncertainty band as 68% interval of the varied histograms
	samples = ['ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8','WZTo3LNu_0Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WZTo3LNu_1Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WZTo3LNu_2Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WZTo3LNu_3Jets_MLL-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','ZZTo4L_13TeV_powheg_pythia8','tZq_ll_4f_13TeV-amcatnlo-pythia8','ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8','WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8','WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8','WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8']

	histnr = 0 #chooses correct file
	hists = []

	c = ROOT.TCanvas('c','c',1000,800)

	infiles = [] # input files for the histograms with varied pdf weights
        mcfiles = [] # input files for the nominal histogram

        for sample in samples:
                mcfiles.append(ROOT.TFile('/home/sfontana/CMSSW_7_1_5/src/CombinedEWKAnalysis/CommonTools/test/VBS_cutbased/VBS_cutbased_with_deltaRcut_allhistos/{0}.root'.format(sample),'read'))
	hist = ROOT.TH1F("hist","hist",1,mcfiles[0].Get('PPP/signal_region/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinLowEdge(binnr),mcfiles[0].Get('PPP/signal_region/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinUpEdge(binnr)) #nominal histogram
	
	weights = []

	for nr in range(9,111):#creates list of pdf weights
		weights.append('genWeight_NNPDF_{0}'.format(nr))

	hists = []

       # up/down histogram of the error band
	hist_upperlimit = ROOT.TH1F("hist_upperlimit","hist_upperlimit",1,mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF1.0/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinLowEdge(binnr),mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF1.0/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinUpEdge(binnr))
	hist_lowerlimit = ROOT.TH1F("hist_lowerlimit","hist_lowerlimit",1,mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF1.0/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinLowEdge(binnr),mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF1.0/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinUpEdge(binnr))

	bin_vector = [] #includes yields for different pdf weights

	for weight in weights: #initializes histograms for all pdf weights
		hists.append(ROOT.TH1F("hist_{0}".format(weight),"hist_{0}".format(weight),1,mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF1.0/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinLowEdge(binnr),mcfiles[0].Get('PPP/signal_region/genWeight_muR1.0_muF1.0/{0}/WZ_mass'.format(channel)).GetXaxis().GetBinUpEdge(binnr)))
               

	for sample in samples: #creates nominal histogram                 
                  hist.AddBinContent(1,mcfiles[histnr].Get('PPP/signal_region/genWeight_muR1.0_muF1.0/{0}/WZ_mass'.format(channel)).GetBinContent(binnr))
                  if (binnr == 8):
                    hist.AddBinContent(1,mcfiles[histnr].Get('PPP/signal_region/genWeight_muR1.0_muF1.0/{0}/WZ_mass'.format(channel)).GetBinContent(9))
                  histnr = histnr + 1
        histnr = 0

	for weightnr in range(len(weights)): #creates varied histograms and adds yiels to the bin-vector
		for sample in samples:
                        infiles.append(ROOT.TFile('/home/sfontana/CMSSW_7_1_5/src/CombinedEWKAnalysis/CommonTools/test/VBS_cutbased/VBS_cutbased_with_deltaRcut_allhistos/{0}.root'.format(sample,weights[weightnr]),'read'))                        
                for sample in samples:
		        hists[weightnr].AddBinContent(1,infiles[histnr].Get('PPP/signal_region/{1}/{0}/WZ_mass'.format(channel,weights[weightnr])).GetBinContent(binnr))		       
		        if (binnr == 8):
                            hists[weightnr].AddBinContent(1,infiles[histnr].Get('PPP/signal_region/{1}/{0}/WZ_mass'.format(channel,weights[weightnr])).GetBinContent(9))
                        infiles[histnr].Close()
                        histnr = histnr + 1
                bin_vector.append(hists[weightnr].GetBinContent(1))
		  
        #uncertainty band is 68% interval, follows https://arxiv.org/abs/1510.03865
        hist_upperlimit.SetBinContent(1,sorted(bin_vector)[84]) 
        hist_lowerlimit.SetBinContent(1,sorted(bin_vector)[16])
        
        #draws histograms to check band
	c.cd() 
	hists[0].Draw()
	for weightnr in range(1,len(weights)):   
		hists[weightnr].Draw("same")


	hist_upperlimit.SetLineColor(ROOT.kRed)
	hist_lowerlimit.SetLineColor(ROOT.kRed)
	hist_upperlimit.Draw("same")
	hist_lowerlimit.Draw("same") 
        hist.SetLineColor(ROOT.kGreen)
        hist.Draw("same hist")

	c.SaveAs("pdf_weights_{0}_bin{1}.png".format(channel,binnr))

        #write histograms to file
	rootfile = ROOT.TFile('/home/sfontana/CMSSW_7_1_5/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/{0}_bin{1}.root'.format(channel,binnr),'UPDATE') 
	hist_upperlimit.SetName("pdf_variationUp")
	hist_lowerlimit.SetName("pdf_variationDown")
	hist_upperlimit.Write('',ROOT.TObject.kOverwrite)
	hist_lowerlimit.Write('',ROOT.TObject.kOverwrite)
	rootfile.Close()
#---------------------------------------------
for c in ['eee','eem','mme','mmm']:
    for b in range(1,9):
        print c, "bin",b
        create_pdf_uncertainties(c,b)

