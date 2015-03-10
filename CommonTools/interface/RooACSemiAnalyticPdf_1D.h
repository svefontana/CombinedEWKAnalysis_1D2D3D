// -*- mode: c++ -*-

#ifndef ROOACSEMIANALYTICPDF_1D
#define ROOACSEMIANALYTICPDF_1D

#include "RooRealProxy.h"
#include "RooAbsPdf.h"
//#include "RooAbsData.h"
#include "TProfile2D.h"
#include "TH1D.h"
#include "TF1.h"
#include "TString.h"
  
class RooACSemiAnalyticPdf_1D : public RooAbsPdf {
public:
  
  enum LimitType{ par1_TH1,
		  par1_TF1,
		  notype };

  RooACSemiAnalyticPdf_1D ();
  RooACSemiAnalyticPdf_1D (const char * name, const char * title,
			   RooAbsReal& _x, 
			   RooAbsReal& _par1, 
			   RooAbsReal& _SM_shape,
			   const char * parFilename,
			   const unsigned& lt);
  RooACSemiAnalyticPdf_1D (const RooACSemiAnalyticPdf_1D& other, const char * name);
  virtual TObject * clone(const char * newname) const { 
    return new RooACSemiAnalyticPdf_1D(*this, newname);
    }
  
  virtual ~RooACSemiAnalyticPdf_1D ();
  
  //  void setLimitType(const unsigned& lt) { type_ = (LimitType)lt; }

  Int_t getAnalyticalIntegral(RooArgSet& allVars, 
			    RooArgSet& analVars, 
			    const char* rangeName = 0) const;

  Double_t analyticalIntegral(Int_t code, const char* rangeName = 0) const;

  void readProfiles(std::vector<double> bins,TDirectory& dir) const ;
  TString getProfileFilename() const { return profileFilename; }
  
protected:
  
  RooRealProxy x;
  RooRealProxy par1;
  RooRealProxy SM_shape;
  
  LimitType type_;

  mutable std::map<std::string,std::vector<double> > integral_basis;

  mutable std::vector<double> bins; 

  TString profileFilename;
  
  TH1D ** P_par1_histo; //!
  TF1 ** P_par1_TF; //!
  
  void initializeProfiles();
  void initializeBins(const RooAbsReal& shape) const;
  void initializeNormalization(const std::string& rName,
			       const RooAbsReal& dep,
			       const RooAbsReal& shape) const;
  void readProfiles(RooACSemiAnalyticPdf_1D const& other);
  
  virtual double evaluate() const ;
  
private:
  
  ClassDef(RooACSemiAnalyticPdf_1D, 4) // aTGC function 
};

#endif
