#include <iostream>
#include <sstream>
#include <string>
using namespace std;

void splitSignal_SMaTGC(TString inputFile){

  ifstream  input(inputFile);
  const int linesize=1024;
  char inbuf[linesize];
  char inbufChain[linesize];
  const int max_files = 200;
  int nfiles=0;
  while (input.getline(inbuf,linesize)) {
    
    //    cout << "read line: " << inbuf << endl;
    if (inbuf[0] == '#') {
      //      cout << "comment \n";
      continue;
    }
    istrstream istline(inbuf);

    TString file_name;
    TString file_withCorrHisto_name;
    TString CorrHisto_name;
    //    vector<TString> errNames;
    TString errNames;
    TString signal_file_name;
    TString channel_name_old;
    TString channel_name_new;

    istline >> file_name
	    >> file_withCorrHisto_name
	    >> CorrHisto_name
	    >> errNames
	    >> signal_file_name
	    >> channel_name_old
	    >> channel_name_new
	    ;

    cout <<"reading file: "<<file_name<< "\t and correcting SM histo by "<< file_withCorrHisto_name<<":"<< CorrHisto_name <<"\t err anmes: "<<errNames<< endl;

    
    std::vector<TString> histos_updown_v;
    if (errNames!="0"){
      TObjArray *strL = errNames.Tokenize(",");
      
      for (int k=0;k<strL->GetLast()+1;k++){
	TString histo=((TObjString *)strL->At(k))->GetString();
	histos_updown_v.push_back(histo);
      }
      delete strL;
    }

  
    // correcting SM histo with file_withCorrHisto:CorrHisto_name
    bool do_corr=false;
    TH1D * histo_corr=new TH1D();
    if (file_withCorrHisto_name!="0" && CorrHisto_name!="0"){
      cout <<"  -> correcting SM histo by "<< file_withCorrHisto_name<<":"<< CorrHisto_name  << endl;
      TFile * file_withCorrHisto=new TFile(file_withCorrHisto_name,"read");
      file_withCorrHisto->cd();
      histo_corr=(TH1D*)(file_withCorrHisto->Get(CorrHisto_name)->Clone("clone_name"));
      do_corr=true;
    }

  TH1D * plot_SM=new TH1D("plot_SM","plot_SM",10,0.,10.);

  TFile * file_in=new TFile(file_name,"read");
  file_in->cd();
  //  file_in->ls();


  TList * list_histos=file_in->GetListOfKeys();
  TString file_out=file_name;
  file_out=file_out.ReplaceAll(channel_name_old,channel_name_new);
  cout <<" ----> output: "<< file_out<<"\n" << endl;
  TFile *outFile=new TFile(file_out,"recreate");
  outFile->cd();

  
  for (int i=0;i<list_histos->GetEntries();i++){
    // read histos one by one
    TString histo_name= list_histos->At(i)->GetName();

    cout <<"\treading histo \""<< histo_name <<"\""<< endl;
    // from "diboson" make: "dibosonSM"="diboson" and "diboson"=histo with all bin contents equal to 1!

    // check if this is one of syst up/down histos affecting signal
    bool signal_syst=false;
    //    int signal_syst=false;
    for (int j=0;j<histos_updown_v.size();j++){
      TString name=histo_name;
      name.ReplaceAll("Up","");
      name.ReplaceAll("Down","");
      if (histos_updown_v[j]==name)
	signal_syst=true;
    }

    if (histo_name=="diboson"){
      cout << "\t -> reading diboson"<< endl;
      // save "diboson" as "dibosonSM"
      TH1D * plot_diboson=(TH1D*)(file_in->Get(histo_name)->Clone("namec"));
      plot_SM=(TH1D*)(file_in->Get(histo_name)->Clone("somename"));
      plot_diboson=(TH1D*)(file_in->Get(histo_name)->Clone("namej"));
      plot_diboson->SetName("dibosonSM");

      // correcting with histo file_withCorrHisto:CorrHisto_name
      if(do_corr){
	plot_diboson->Multiply(histo_corr);
      }

      plot_diboson->Write();

 
      plot_SM->Write("dibosonSM_origi");

      // create "diboson" histo with all bin contents equal to 1!
      TH1D * plot_aTGC=(TH1D*)(file_in->Get(histo_name)->Clone("name_histo_atgc"));
      plot_aTGC->SetName("diboson");
      int N_bins=plot_aTGC->GetNbinsX();
      for (int j=1;j<=N_bins;j++)
	plot_aTGC->SetBinContent(j,1.);
      plot_aTGC->Write();


      // make corr_err histos on SM and aTGC -> relative error from correction histo
      if(do_corr){

	// SM:
	TH1D * plot_SM_up=(TH1D*)(plot_diboson->Clone("name_histo_atgcX"));
	for (int j=1;j<=N_bins;j++){
	  plot_SM_up->SetBinContent(j,plot_SM_up->GetBinContent(j)*(1.+histo_corr->GetBinError(j)/histo_corr->GetBinContent(j)));
	}
	plot_SM_up->Write("CMS_hzz2l2v_ewkUp");

	TH1D * plot_SM_down=(TH1D*)(plot_diboson->Clone("name_histo_atgcX"));
	for (int j=1;j<=N_bins;j++){
	  plot_SM_down->SetBinContent(j,plot_SM_down->GetBinContent(j)*(1.-histo_corr->GetBinError(j)/histo_corr->GetBinContent(j)));
	}
	plot_SM_down->Write("CMS_hzz2l2v_ewkDown");

	// aTGC:
	TH1D * plot_aTGC_up=(TH1D*)(plot_aTGC->Clone("name_histo_atgcX"));
	for (int j=1;j<=N_bins;j++){
	  plot_aTGC_up->SetBinContent(j,plot_aTGC_up->GetBinContent(j)*(1.+histo_corr->GetBinError(j)/histo_corr->GetBinContent(j)));
	}
	plot_aTGC_up->Write("diboson_corrUp");

	TH1D * plot_aTGC_down=(TH1D*)(plot_aTGC->Clone("name_histo_atgcX2"));
	for (int j=1;j<=N_bins;j++){
	  plot_aTGC_down->SetBinContent(j,plot_aTGC_down->GetBinContent(j)*(1.-histo_corr->GetBinError(j)/histo_corr->GetBinContent(j)));
	}
	plot_aTGC_down->Write("diboson_corrDown");

      }
     
    }
    else if (signal_syst) { // if this is signal syst then save this and create aTGC syst plot with the same relative error 
      cout << "\t -> reading signal unc"<< endl;
      TH1D* plot_unc=(TH1D*)(file_in->Get(histo_name)->Clone("name_histo_atgc2"));
      int N_bins=plot_unc->GetNbinsX();
      
      TString name_origi_syst=histo_name;
      name_origi_syst=name_origi_syst.ReplaceAll("Up","origiUp");
      name_origi_syst=name_origi_syst.ReplaceAll("Down","origiDown");
      plot_unc->Write(name_origi_syst);


      plot_unc->Multiply(histo_corr);
      TString name_SM_syst=histo_name;
      name_SM_syst=name_SM_syst.ReplaceAll("Up","SMUp");
      name_SM_syst=name_SM_syst.ReplaceAll("Down","SMDown");
      plot_unc->Write(name_SM_syst);

      TH1D * plotSM=(TH1D*)(file_in->Get("diboson")->Clone("name_histo_atgc3"));
       for (int j=1;j<=N_bins;j++){
	plot_unc->SetBinContent(j,plot_unc->GetBinContent(j)/plot_diboson->GetBinContent(j));
      }
      TString name_atgc_syst=histo_name;
      name_atgc_syst=name_atgc_syst.ReplaceAll("Up","aTGCUp");
      name_atgc_syst=name_atgc_syst.ReplaceAll("Down","aTGCDown");
     plot_unc->Write(histo_name);
      cout << "\t\t -> saving as: "<< name_atgc_syst<< endl;
    }     
    else{ // simply save histo
      TH1D * plot=(TH1D*)(file_in->Get(histo_name)->Clone("name_histo_atgc4"));
      int N_bins=plot->GetNbinsX();
      plot->Write(histo_name);
    }

  }

  cout <<" ---> reading signal file: "<< signal_file_name << endl;
  
  TFile * file_in_signal=new TFile(signal_file_name,"read");
  file_in_signal->cd();
  //  file_in_signal->ls();

  TList * list_histos_signal=file_in_signal->GetListOfKeys();
  TString file_out_signal=signal_file_name;
  file_out_signal=file_out_signal.ReplaceAll(channel_name_old,channel_name_new);
  cout <<" ----> output: "<< file_out_signal<<"\n" << endl;
  TFile *outFile_signal=new TFile(file_out_signal,"recreate");
  outFile_signal->cd();


  TH2D * histo_1=new TH2D();
  histo_1=(TH2D*)(file_in_signal->Get("bin_content_lam_dk_1")->Clone("something"));
  for (int i=1;i<=histo_1->GetNbinsX();i++)
    for (int j=1;j<=histo_1->GetNbinsY();j++)
      histo_1->SetBinContent(i,j,-1.);
 
  int N_signal_histos=0;
  for (int i=0;i<list_histos_signal->GetEntries();i++){
    // read histos one by one
    TString histo_name= list_histos_signal->At(i)->GetName();
    cout <<"\treading histo \""<< histo_name <<"\""<< endl;

     if (!histo_name.Contains("_lam_dk_"))
      continue;

    N_signal_histos++;
    TH2D * plot_signal=(TH2D*)(file_in_signal->Get(histo_name)->Clone("namec2"));
    plot_signal->Add(histo_1);
    plot_signal->Scale(plot_SM->GetBinContent(N_signal_histos));

    // check if signal<0->setTo0!
    
    for (int ii=1;ii<=histo_1->GetNbinsX();ii++){
      for (int jj=1;jj<=histo_1->GetNbinsY();jj++){
	if (plot_signal->GetBinContent(ii,jj)<0.){
	  //	  cout <<"~~~~~~~~~~~~~~~~~ found bin with signal<0 -> setTo0! "<< histo_name<<" bin: "<< i<<","<<j << endl;
	  plot_signal->SetBinContent(ii,jj,0.);
	}
      }
    }
    

    plot_signal->Write(histo_name);
    delete plot_signal;


  }




  }
  
  outFile->Close();
  outFile_signal->Close();
  file_in->Close();
  

}
