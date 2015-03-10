void make_1and2sigmaExp(TString file_exp_toys,int N_points, int N_toys, double asimov_down, double asimov_up){

  gROOT->ProcessLine(".L CMSStyle.C");
  gROOT->ProcessLine("CMSStyle()");
  gROOT->LoadMacro("CMSStyle.C");
  CMSStyle();

  TString output_plot_name="limit_1D_expected12sigma";

  /*
  double asimov_down=-0.176;
  double asimov_up=0.242;
  */

  //  TFile * file_in=new TFile("higgsCombineTest.MultiDimFit.mH120.123456_200toys_400points.root","read");
  TFile * file_in=new TFile(file_exp_toys,"read");
  file_in->cd();
  //  int N_points=400.;
  //  int N_toys=200.;
  double min_par=-0.6;
  double max_par=0.6;
  double Mean_value=0.5;
  double sigma1_value_down=0.16;
  double sigma1_value_high=0.84;
  double sigma2_value_down=0.025;
  double sigma2_value_high=0.975;

  double Mean_value_up=-1.;
  double sigma1_value_down_up=-1.;
  double sigma1_value_high_up=-1.;
  double sigma2_value_down_up=-1.;
  double sigma2_value_high_up=-1.;

  double Mean_value_down=-1.;
  double sigma1_value_down_down=-1.;
  double sigma1_value_high_down=-1.;
  double sigma2_value_down_down=-1.;
  double sigma2_value_high_down=-1.;

  std::vector<double> Mean_limit;
  std::vector<double> sigma1_down_limit;
  std::vector<double> sigma1_high_limit;
  std::vector<double> sigma2_down_limit;
  std::vector<double> sigma2_high_limit;
  
  
  TH1F * histo=new TH1F("histo","histo",N_points,min_par,max_par);
  limit->Draw("lZ>>histo","abs(deltaNLL)<1.92");
  histo->Scale(1./double(N_toys));
  histo->Draw();

  bool lastBelowErrMean = false;
  bool lastAboveErrMean = true;

  double boundsMean_yield=-100.;
  double boundsMean=-100.;



  bool lastBelowErrsigma1_down = false;
  bool lastAboveErrsigma1_down = true;

  double boundssigma1_down_yield=-100.;
  double boundssigma1_down=-100.;
  

  bool lastBelowErrsigma1_high = false;
  bool lastAboveErrsigma1_high = true;

  double boundssigma1_high_yield=-100.;
  double boundssigma1_high=-100.;
  


  bool lastBelowErrsigma2_down = false;
  bool lastAboveErrsigma2_down = true;

  double boundssigma2_down_yield=-100.;
  double boundssigma2_down=-100.;
  

  bool lastBelowErrsigma2_high = false;
  bool lastAboveErrsigma2_high = true;

  double boundssigma2_high_yield=-100.;
  double boundssigma2_high=-100.;
  

  for (int i=1;i<histo->GetNbinsX()+1;i++){
    double yield=histo->GetBinContent(i);
    double par=histo->GetBinCenter(i);

    // find mean
    if (yield<Mean_value){
      if (lastAboveErrMean){
	boundsMean_yield=yield;
	boundsMean=par;
	Mean_limit.push_back(par);
      }
      lastBelowErrMean = true;
      lastAboveErrMean = false;
    }
    else{
      if (lastBelowErrMean){
	boundsMean_yield=yield;
	boundsMean=par;
	Mean_limit.push_back(par);
      }
      lastBelowErrMean = false;
      lastAboveErrMean = true;
    }

    // find 1sigma down
    if (yield<sigma1_value_down){
      if (lastAboveErrsigma1_down){
	boundssigma1_down_yield=yield;
	boundssigma1_down=par;
	sigma1_down_limit.push_back(par);
      }
      lastBelowErrsigma1_down = true;
      lastAboveErrsigma1_down = false;
    }
    else{
      if (lastBelowErrsigma1_down){
	boundssigma1_down_yield=yield;
	boundssigma1_down=par;
	sigma1_down_limit.push_back(par);
      }
      lastBelowErrsigma1_down = false;
      lastAboveErrsigma1_down = true;
    }


    // find 1sigma high
    if (yield<sigma1_value_high){
      if (lastAboveErrsigma1_high){
	boundssigma1_high_yield=yield;
	boundssigma1_high=par;
	sigma1_high_limit.push_back(par);
      }
      lastBelowErrsigma1_high = true;
      lastAboveErrsigma1_high = false;
    }
    else{
      if (lastBelowErrsigma1_high){
	boundssigma1_high_yield=yield;
	boundssigma1_high=par;
	sigma1_high_limit.push_back(par);
      }
      lastBelowErrsigma1_high = false;
      lastAboveErrsigma1_high = true;
    }


    // find 2sigma down
    if (yield<sigma2_value_down){
      if (lastAboveErrsigma2_down){
	boundssigma2_down_yield=yield;
	boundssigma2_down=par;
	sigma2_down_limit.push_back(par);
      }
      lastBelowErrsigma2_down = true;
      lastAboveErrsigma2_down = false;
    }
    else{
      if (lastBelowErrsigma2_down){
	boundssigma2_down_yield=yield;
	boundssigma2_down=par;
	sigma2_down_limit.push_back(par);
      }
      lastBelowErrsigma2_down = false;
      lastAboveErrsigma2_down = true;
    }


    // find 2sigma high
    if (yield<sigma2_value_high){
      if (lastAboveErrsigma2_high){
	boundssigma2_high_yield=yield;
	boundssigma2_high=par;
	sigma2_high_limit.push_back(par);
      }
      lastBelowErrsigma2_high = true;
      lastAboveErrsigma2_high = false;
    }
    else{
      if (lastBelowErrsigma2_high){
	boundssigma2_high_yield=yield;
	boundssigma2_high=par;
	sigma2_high_limit.push_back(par);
      }
      lastBelowErrsigma2_high = false;
      lastAboveErrsigma2_high = true;
    }


    
  }
    
  cout << "boundsMean= "
    //<< boundsMean_yield<<" -> "<<boundsMean<< "\n  -> vector: "
       << endl;
  for (int i=0;i<Mean_limit.size();i++)
    cout <<"\t" <<Mean_limit[i];

  cout << endl;
    
  cout << "boundssigma1_down= "
    //<< boundssigma1_down_yield<<" -> "<<boundssigma1_down<< "\n  -> vector: "
       << endl;
  for (int i=0;i<sigma1_down_limit.size();i++)
    cout <<"\t" <<sigma1_down_limit[i];
  cout << endl;
    
  cout << "boundssigma1_high= "
    //       << boundssigma1_high_yield<<" -> "<<boundssigma1_high<< "\n  -> vector: "
       << endl;
  for (int i=0;i<sigma1_high_limit.size();i++)
    cout <<"\t" <<sigma1_high_limit[i];
  cout << endl;
    
  cout << "boundssigma2_down= "
    //<< boundssigma2_down_yield<<" -> "<<boundssigma2_down<< "\n  -> vector: "
       << endl;
  for (int i=0;i<sigma2_down_limit.size();i++)
    cout <<"\t" <<sigma2_down_limit[i];
  cout << endl;
    
  cout << "boundssigma2_high= "
    //<< boundssigma2_high_yield<<" -> "<<boundssigma2_high<< "\n  -> vector: "
       << endl;
  for (int i=0;i<sigma2_high_limit.size();i++)
    cout <<"\t" <<sigma2_high_limit[i];
  cout << endl;

  
  TCanvas *c2 = new TCanvas("c2","A Simple Graph with error bars",200,10,700,500) ;
    
  //  c2->SetFillColor(42) ;
  c2->SetGrid(0,1) ;
  //  c2->GetFrame()->SetFillColor(21) ;
  c2->GetFrame()->SetBorderSize(12) ;
    // create the arrays for the points
  const Int_t n = 1 ;
  Double_t x[n] = {0.5} ;
  Double_t y[n] = {0.}; 
// create the arrays with high and low errors
  Double_t exl[n] = {.0} ;
  Double_t eyl[n] = {-1.*asimov_down} ;
  Double_t exh[n] = {.0} ;
  Double_t eyh[n] = {asimov_up} ;

  const Int_t nMean = 2 ;
  Double_t xMean[nMean] = {0.4,0.6} ;
  Double_t yMean[nMean] = {0.,0.}; 
// create the arrays with high and low errors
  Double_t exlMean[nMean] = {0.,0.} ;
  Double_t eylMean[nMean] = {fabs(Mean_limit[1]), fabs(Mean_limit[1])} ;
  Double_t exhMean[nMean] = {0., 0.} ;
  Double_t eyhMean[nMean] = {Mean_limit[2], Mean_limit[2]} ;

  cout << "\n\t\tplotting:"<< endl;
  cout <<"Mean: "<< Mean_limit[1]<<" "<< Mean_limit[2] << endl;

  const Int_t n2sig = 2 ;
  Double_t x2sig[n2sig] = {0.4,0.6} ;
  Double_t y2sig[n2sig] = {0.,0.}; 
// create the arrays with high and low errors
  Double_t exl2sig[n2sig] = {0.,0.} ;
  Double_t eyl2sig[n2sig] = {fabs(sigma2_down_limit[1]), fabs(sigma2_down_limit[1])} ;
  Double_t exh2sig[n2sig] = {.0, 0.} ;
  Double_t eyh2sig[n2sig] = {sigma2_down_limit[2], sigma2_down_limit[2]} ;

  cout <<"2sigma: "<<sigma2_down_limit[1] <<" "<< sigma2_down_limit[2] << endl;

  const Int_t n1sig_up = 2 ;
  Double_t x1sig_up[n1sig_up] = {0.4,0.6} ;
  Double_t y1sig_up[n1sig_up] = {0.,0.}; 
// create the arrays with high and low errors
  Double_t exl1sig_up[n1sig_up] = {0.,0.} ;
  Double_t eyl1sig_up[n1sig_up] = {fabs(sigma1_down_limit[1]), fabs(sigma1_down_limit[1])} ;
  Double_t exh1sig_up[n1sig_up] = {.0, 0.} ;
  Double_t eyh1sig_up[n1sig_up] = {sigma1_high_limit[1], sigma1_high_limit[1]} ;

  cout <<"1sigma: "<< sigma1_down_limit[1]<<" "<<sigma1_high_limit[1]  << endl;

  const Int_t n1sig_down = 2 ;
  Double_t x1sig_down[n1sig_down] = {0.4,0.6} ;
  Double_t y1sig_down[n1sig_down] = {0.,0.}; 
// create the arrays with high and low errors
  Double_t exl1sig_down[n1sig_down] = {0.,0.} ;
  Double_t eyl1sig_down[n1sig_down] = {-1.*(sigma1_high_limit[2]), -1.*(sigma1_high_limit[2])} ;
  Double_t exh1sig_down[n1sig_down] = {.0, 0.} ;
  Double_t eyh1sig_down[n1sig_down] = {sigma1_down_limit[2], sigma1_down_limit[2]} ;

  cout <<"1sigma: "<< sigma1_high_limit[2]<<" "<<sigma1_down_limit[2]  << endl;
  
  gr2sigma = new TGraphAsymmErrors(n2sig,x2sig,y2sig,exl2sig,exh2sig,eyl2sig,eyh2sig) ;
  gr2sigma->SetTitle("TGraphAsymmErrors Example") ;
  gr2sigma->SetMarkerColor(4) ;
  gr2sigma->SetMarkerStyle(21) ;
  gr2sigma->SetFillColor(kYellow) ;
  gr2sigma->SetLineColor(kYellow) ;
  gr2sigma->GetYaxis()->SetTitle("parameter") ;
  gr2sigma->GetXaxis()->SetLabelColor(0) ;
  TAxis *axis = gr2sigma->GetXaxis();
  //  axis->SetLimits(0.,1.); 
  axis->SetLimits(0.2,1.); 
  gr2sigma->DrawClone("E3AL") ;
  
  
  grMean = new TGraphAsymmErrors(nMean,xMean,yMean,exlMean,exhMean,eylMean,eyhMean) ;
  grMean->SetTitle("TGraphAsymmErrors Example") ;
  grMean->SetMarkerColor(4) ;
  grMean->SetMarkerStyle(21) ;
  grMean->SetFillColor(kRed) ;
  grMean->SetLineColor(kRed) ;
  //  grMean->SetFillStyle(3010) ;
  grMean->SetFillStyle(3005) ;
  grMean->SetLineColor(kRed) ;
  
  gr1sigma_up = new TGraphAsymmErrors(n1sig_up,x1sig_up,y1sig_up,exl1sig_up,exh1sig_up,eyl1sig_up,eyh1sig_up) ;
  gr1sigma_up->SetTitle("TGraphAsymmErrors Example") ;
  gr1sigma_up->SetMarkerColor(4) ;
  gr1sigma_up->SetMarkerStyle(21) ;
  gr1sigma_up->SetFillColor(kGreen) ;
  gr1sigma_up->SetLineColor(kGreen) ;
  gr1sigma_up->DrawClone("E3Same") ;
  
  gr1sigma_down = new TGraphAsymmErrors(n1sig_down,x1sig_down,y1sig_down,exl1sig_down,exh1sig_down,eyl1sig_down,eyh1sig_down) ;
  gr1sigma_down->SetTitle("TGraphAsymmErrors Example") ;
  gr1sigma_down->SetMarkerColor(4) ;
  gr1sigma_down->SetMarkerStyle(21) ;
  gr1sigma_down->SetLineColor(kGreen) ;
  gr1sigma_down->SetFillColor(kGreen) ;
  gr1sigma_down->DrawClone("E3Same") ;
  

 // create TGraphAsymmErrors with the arrays
  gr = new TGraphAsymmErrors(n,x,y,exl,exh,eyl,eyh) ;
  gr->SetTitle("TGraphAsymmErrors Example") ;
  //  gr->SetMarkerColor(4) ;
  //  gr->SetMarkerStyle(21) ;
  //  gr->Draw("ALP") ;
  gr->Draw("Same") ;

  //  grMean->DrawClone("LSame") ;
  grMean->DrawClone("E3Same") ;


  gPad->RedrawAxis(); // in the end of your macro


    TLegend *leg = new TLegend(0.65, 0.6, 0.85, 0.85);
   leg->SetHeader("95% CL");
   leg->SetFillColor(0);
   leg->SetFillStyle(0);
   leg->SetShadowColor(0);
   leg->SetBorderSize(0);
   leg->SetTextFont(132);
   leg->SetTextSize(0.035);
   leg->AddEntry(gr, "Asimov expected limit","l");
   leg->AddEntry(grMean, "Mean expected limit","f");
   leg->AddEntry(gr1sigma_up, "#pm 1#sigma expected limit","f");
   leg->AddEntry(gr2sigma, "#pm 2#sigma expected limit","f");
   leg->Draw();
 
   c2->SaveAs(output_plot_name+".root");
   c2->SaveAs(output_plot_name+".pdf");
   c2->SaveAs(output_plot_name+".C");

}
