// -*- mode: c++ -*-


#ifndef ROOACPROCESSSCALING_1D
#define ROOACPROCESSSCALING_1D

#include "RooRealProxy.h"
#include "RooAbsPdf.h"
#include "TProfile2D.h"
#include "TH1D.h"
#include "TF1.h"
#include "TString.h"
#include <iostream>
#include <fstream>
#include <vector>

  
class RooACProcessScaling_1D : public RooAbsReal {
public:
  
  enum LimitType{ par1_TH1, 
		  par1_TF1, 
		  notype };

  RooACProcessScaling_1D ();
  RooACProcessScaling_1D (const char * name, const char * title,
			 RooAbsReal& _x, RooAbsReal& _par1,
			 RooAbsReal& _SM_shape,
				   const char * parFilename,LimitType _type);
  RooACProcessScaling_1D (const RooACProcessScaling_1D& other, const char * name);
  virtual TObject * clone(const char * newname) const { 
    return new RooACProcessScaling_1D(*this, newname);
    }
  
  //  void setLimitType(const unsigned& lt) { type_ = (LimitType)lt; }

  virtual ~RooACProcessScaling_1D ();  
  
  void readProfiles(std::vector<double> bins,TDirectory& dir,LimitType _type) const ;

  TString getProfileFilename() const { return profileFilename; }
  
protected:
  
  RooRealProxy par1;
  
  LimitType type_;

  double SM_integral;
  std::vector<double> integral_basis;
  std::vector<double> bins;

  TString profileFilename;
  
  TH1D ** P_par1_histo; //! 
  TF1 ** P_par1_TF; //!
  
  void initializeProfiles();
  void initializeNormalization(const RooAbsReal& dep,
			       const RooAbsReal& shape);
  void readProfiles(RooACProcessScaling_1D const& other);
  
  virtual double evaluate() const ;
  
private:
  
  ClassDef(RooACProcessScaling_1D, 3) // aTGC function 
};

#endif
