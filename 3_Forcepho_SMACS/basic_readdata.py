import os, sys, glob, shutil
import argparse, logging
import numpy as np
import json, yaml

from astropy.io import fits

from config import main_config_parser

from forcepho.patches import FITSPatch, CPUPatchMixin
from forcepho.superscene import LinkedSuperScene
from forcepho.utils import NumpyEncoder, write_to_disk
from forcepho.fitting import run_lmc


from demo_utils import get_parser
from demo_utils import make_stamp, make_scene
from demo_utils import get_galsim_psf, galsim_model, compute_noise_level
from demo_utils import make_psfstore, write_fits_to



class Patcher(FITSPatch, CPUPatchMixin):
    pass 


def make_tag(config):
    tag = f"sersic{config.sersic[0]:.1f}_rhalf{config.rhalf[0]:.3f}"
    tag += f"_snr{config.snr:03.0f}_noise{config.add_noise:.0f}"
    return tag


parser = main_config_parser() #get_parser()
parser.set_defaults(bands=["CLEAR"],
                    scales=[0.03],
                    sigma_psf=[2.5],
                    rhalf=[0.2],
                    sersic=[2.0])
parser.add_argument("--tag", type=str, default="")
parser.add_argument("--scales", type=float, nargs="*", default=[0.03])
parser.add_argument("--bands", type=str, nargs="*", default=["CLEAR"])
parser.add_argument("--nx", type=int, default=64)
parser.add_argument("--ny", type=int, default=64)
# scene
parser.add_argument("--rhalf", type=float, nargs="*", default=[0.2, 0.2], help="arcsec")
parser.add_argument("--sersic", type=float, nargs="*", default=[2.0])
parser.add_argument("--flux", type=float, nargs="*", default=[1.0])
parser.add_argument("--q", type=float, nargs="*", default=[0.9])
parser.add_argument("--pa", type=float, nargs="*", default=[np.pi/2])
parser.add_argument("--dist_frac", type=float, default=1.5)
# PSF
parser.add_argument("--sigma_psf", type=float, nargs="*", default=[3.0], help="in pixels")
parser.add_argument("--psfstore", type=str, default="./single_gauss_psf.h5")
# MOre
parser.add_argument("--snr", type=float, default=50, help="S/N within rhalf")
parser.add_argument("--add_noise", type=int, default=1)
parser.add_argument("--outdir", type=str, default=[])



config = parser.parse_args()
config.image_name = f"{config.fitsfiles[0]}"
# config.tag = make_tag(config) #파일이름 붙이는 것 
#config.outdir = os.path.join("./tests2/", config.tag)
config.outdir = os.path.join(config.outdir, config.tag)
os.makedirs(config.outdir, exist_ok=True)

outroot = os.path.join(config.outdir, config.tag)
band, sigma, scale = config.bands[0], config.sigma_psf[0], config.scales[0]



cat = fits.getdata(config.image_name, -1)
bands = fits.getheader(config.image_name, -1)["FILTERS"].split(",")
# bands = fits.getdata(config.image_name, -1)['FILTERS'].split(",")
sceneDB = LinkedSuperScene(sourcecat=cat, 
                            bands=bands,
                            statefile=os.path.join(config.outdir, 
                            "final_scene.fits"), 
                            roi=cat["rhalf"] * 5,       
                            bounds_kwargs=dict(n_pix=1.0), 
                            target_niter=config.sampling_draws)

# load the image data
patcher = Patcher(fitsfiles=[config.image_name],
                    psfstore=config.psfstore,
                    splinedata=config.splinedatafile,
                    return_residual=True)

# check out scene & bounds
region, active, fixed = sceneDB.checkout_region(seed_index=-1)
bounds, cov = sceneDB.bounds_and_covs(active["source_index"])

# prepare model and data, and sample
print(bands)
patcher.build_patch(region, None, allbands=bands)
model, q = patcher.prepare_model(active=active, fixed=fixed,
                                    bounds=bounds, shapes=sceneDB.shape_cols)
out, step, stats = run_lmc(model, q.copy(),
                            n_draws=config.sampling_draws,
                            warmup=config.warmup,
                            z_cov=cov, full=True,
                            weight=max(10, active["n_iter"].min()),
                            discard_tuned_samples=False,
                            max_treedepth=config.max_treedepth,
                            progressbar=config.progressbar)

# Check results back in and end
final, covs = out.fill(region, active, fixed, model, bounds=bounds,
                        step=step, stats=stats, patchID=0)
write_to_disk(out, outroot, model, config)
sceneDB.checkin_region(final, fixed, config.sampling_draws,
                        block_covs=covs, taskID=0)
sceneDB.writeout()