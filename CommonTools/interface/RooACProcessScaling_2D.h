// -*- mode: c++ -*-


#ifndef ROOACPROCESSSCALING_2D
#define ROOACPROCESSSCALING_2D

#include "RooRealProxy.h"
#include "RooAbsPdf.h"
#include "TProfile2D.h"
#include "TH2D.h"
#include "TF2.h"
#include "TString.h"
#include <iostream>
#include <fstream>
#include <vector>

  
class RooACProcessScaling_2D : public RooAbsReal {
public:
  
  enum LimitType{ par1par2_TF2par, 
		  par1par2_TH2, 
		  par1par2_TF2, 
		  notype };

  RooACProcessScaling_2D ();
  RooACProcessScaling_2D (const char * name, const char * title,
			 RooAbsReal& _x, RooAbsReal& _par1,
			 RooAbsReal& _par2, 
			 RooAbsReal& _SM_shape,
				   const char * parFilename,LimitType _type);
  RooACProcessScaling_2D (const RooACProcessScaling_2D& other, const char * name);
  virtual TObject * clone(const char * newname) const { 
    return new RooACProcessScaling_2D(*this, newname);
    }
  
  //  void setLimitType(const unsigned& lt) { type_ = (LimitType)lt; }

  virtual ~RooACProcessScaling_2D ();  
  
  //here:
  //  void readProfiles(const RooAbsReal& dep,TDirectory& dir) const ;
  void readProfiles(std::vector<double> bins,TDirectory& dir,LimitType _type) const ;

  TString getProfileFilename() const { return profileFilename; }
  
protected:
  
  RooRealProxy par1;
  RooRealProxy par2;
  
  LimitType type_;

  double SM_integral;
  std::vector<double> integral_basis;
  std::vector<double> bins;

  TString profileFilename;
  
  TH2D ** P_par1par2_histo; //!
  TF2 ** P_par1par2_TF; //!
  
  void initializeProfiles();
  void initializeNormalization(const RooAbsReal& dep,
			       const RooAbsReal& shape);
  void readProfiles(RooACProcessScaling_2D const& other);
  
  virtual double evaluate() const ;
  
private:
  
  ClassDef(RooACProcessScaling_2D, 3) // aTGC function 
};

#endif
