# JWST / HST Galaxy Analysis

A learning project for galaxy morphology and photometry using JWST and HST imaging data.

## Overview

This repository contains exploratory workflows for:
- **Morpheus** — Deep learning-based pixel-level morphological classification (spheroid, disk, irregular, point source)
- **Photutils + SExtractor** — Image alignment, FWHM estimation, and ellipse/spiral isophote fitting
- **Forcepho** — Bayesian Sérsic galaxy fitting with PSF modeling (SMACS J0723)

*Note: This project is a summary of code and studies from my 2022 internship. At that time, I organized scripts and exploratory notebooks as I worked. However, the data files used during the internship were lost afterwards, so it is no longer possible to fully reproduce or rerun the workflows as originally intended. The code and analyses are preserved here mainly for study and record-keeping purposes, and some pipelines may be incomplete or not fully functional as a result.*

---

## Project Structure

```
2022_JWST_HST_GalaxyAnalysis/
│
├── 1_Morpheus_Morphology/          # Morpheus morphological classification
│   ├── run_Morpheus_main.ipynb     # Main pipeline (H, J, V, z bands → classify → catalog)
│   ├── demo_bigdata_calibration.ipynb
│   │
│   ├── Full_vs_Cutout_SpeedTest/   # Speed comparison: full image vs source-centered cutouts
│   ├── HST_Relics/                 # HST Relics survey galaxies (Total / Centercut)
│   ├── JWST_Cutout/                # JWST CEERS cutout analysis, source-based detection
│   └── Morphology_Validation/      # Visual vs Morpheus(Official) vs Morpheus(me)
│       ├── 3D-HST/                 # 3D-HST EGS catalog comparison
│       └── JWST-CEERS(roberston+2022)/
│
├── 2_Photutils_EllipseFitting/     # Photometry & isophote fitting
│   ├── Photutils/                  # Main pipeline: align → SExtractor → ellipse/spiral fit
│   │   ├── 1_image_align.ipynb     # Astroalign (≥30 point matching)
│   │   ├── 2_SExtractor_FWHM/      # FWHM estimation via SExtractor
│   │   │   ├── filters_F115W_F150W/, F115WF200W/, F150WF200W/
│   │   │   └── sextractor_config/
│   │   ├── 3_ellipse_fitting.ipynb
│   │   ├── 3_spiral_fitting.ipynb
│   │   └── cutout_images/
│   └── Morpheus_Classification/    # Morpheus on Photutils images (ellipse/spiral types)
│
└── 3_Forcepho_SMACS/              # Forcepho Bayesian galaxy fitting
    ├── config.py, demo_utils.py, basic_readdata.py, basic_plot_edit.py
    ├── cut_JWSTimg.ipynb
    ├── raw_fits_catalog_gen.ipynb
    ├── run_basic_readdata.ipynb
    ├── img/                        # JWST NIRCam cutouts, Robertson+ source
    ├── psf/                        # PSF Gaussian mixture fits (make_psf.py)
    └── sersic_splinedata_large.h5
```

