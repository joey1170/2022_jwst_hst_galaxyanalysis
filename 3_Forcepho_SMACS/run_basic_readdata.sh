ln -s /data/jip/2nd_TASK/forcepho/demo/demo_utils.py demo_utils.py
ln -s /data/jip/2nd_TASK/forcepho/demo/data/sersic_splinedata_large.h5 sersic_splinedata_large.h5
ln -s /data/jip/2nd_TASK/run_forcepho/config.py config.py
export SPS_HOME="/data/jip/2nd_TASK/fsps"
export LD_LIBRARY_PATH=/opt/gcc-10.2.1/usr/lib64
python basic_readdata.py --tag sample11 --splinedatafile /data/jip/2nd_TASK/run_forcepho/sersic_splinedata_large.h5 --psfstore /data/jip/2nd_TASK/run_SMACS_forcepho_JWST.ver.Img/psf/sersic1.6_rhalf0.080_snr100_F115Wadd_noise0_psf.h5 --fitsfiles /data/jip/2nd_TASK/run_SMACS_forcepho_JWST.ver.Img/img/f115w_JWST_cutout.fits --outdir ./output --bands CLEAR
