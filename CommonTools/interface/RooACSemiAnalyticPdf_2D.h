// -*- mode: c++ -*-

#ifndef ROOACSEMIANALYTICPDF_2D
#define ROOACSEMIANALYTICPDF_2D

#include "RooRealProxy.h"
#include "RooAbsPdf.h"
//#include "RooAbsData.h"
#include "TProfile2D.h"
#include "TH2D.h"
#include "TF2.h"
#include "TString.h"
  
class RooACSemiAnalyticPdf_2D : public RooAbsPdf {
public:
  
  enum LimitType{ par1par2_TF2par,
		  par1par2_TH2,
		  par1par2_TF2,
		  notype };

  RooACSemiAnalyticPdf_2D ();
  RooACSemiAnalyticPdf_2D (const char * name, const char * title,
			     RooAbsReal& _x, 
			     RooAbsReal& _par1, 
			     RooAbsReal& _par2,
			     RooAbsReal& _SM_shape,
			     const char * parFilename,
			     const unsigned& lt);
  RooACSemiAnalyticPdf_2D (const RooACSemiAnalyticPdf_2D& other, const char * name);
  virtual TObject * clone(const char * newname) const { 
    return new RooACSemiAnalyticPdf_2D(*this, newname);
    }
  
  virtual ~RooACSemiAnalyticPdf_2D ();
  
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
  RooRealProxy par2;
  RooRealProxy SM_shape;
  
  LimitType type_;

  mutable std::map<std::string,std::vector<double> > integral_basis;

  mutable std::vector<double> bins;

  TString profileFilename;
  
  TH2D ** P_par1par2_histo; //!
  TF2 ** P_par1par2_TF; //!
  
  void initializeProfiles();
  void initializeBins(const RooAbsReal& shape) const;
  void initializeNormalization(const std::string& rName,
			       const RooAbsReal& dep,
			       const RooAbsReal& shape) const;
  void readProfiles(RooACSemiAnalyticPdf_2D const& other);
  
  virtual double evaluate() const ;
  
private:
  
  ClassDef(RooACSemiAnalyticPdf_2D, 2) // aTGC function 
};

#endif
