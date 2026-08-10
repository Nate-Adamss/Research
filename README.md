# Research Pipelines

Data engineering pipelines developed during undergraduate 
astrophysics research at the University of Oklahoma. Several 
of these pipelines supported research on a turning-on Active 
Galactic Nucleus (AGN) candidate in galaxy NGC 6447, currently 
under peer review at The Astrophysical Journal 
(arXiv:2602.21502).

---

## Pipelines

### NEOWISE Infrared Light Curve Pipeline
Retrieves multi-epoch infrared photometry from the WISE/NEOWISE 
archive via IRSA, applies MAD-based outlier rejection and 180-day 
epoch binning to produce cleaned, science-ready light curves, and 
filters sources by variability threshold. Output: flux vs. time 
light curves across a 14-year observational baseline.

**Key methods:** cone search queries, sigma-clipping, 
MAD filtering, epoch binning, variability selection

---

### FITS File Flux Analysis
Processes astronomical FITS image files to extract spatial flux 
distributions across a galaxy. Computes flux ratios between 
user-defined regions to identify and characterize the brightest 
structures relative to surrounding areas.

**Key methods:** FITS I/O, aperture photometry, 
spatial masking, flux ratio computation

---

### AGN Color-Color Classification Pipeline
Retrieves W1, W2, and W3 band photometry from AllWISE via 
astroquery, computes infrared color indices (W1−W2, W2−W3), 
and plots source color evolution over time against established 
AGN selection boundaries (Jarrett 2011, Mateos 2012, Stern 2012, 
Blecha 2018, Hviding 2022). Used to identify AGN candidates 
via infrared color classification.

**Key methods:** IRSA cone search queries, W3 photometry 
retrieval, color index computation, multi-epoch color 
evolution plotting.

---

### Proper Motion & Parallax Utility
Computes total proper motion from RA and Dec components using 
standard error propagation, and returns parallax as a proxy 
for source distance. Accepts CSV input or a pandas DataFrame 
and handles missing data gracefully.

**Key methods:** quadrature error propagation, 
pandas I/O, NaN handling

---

## Tech Stack

- **Language:** Python 3
- **Core Libraries:** NumPy, Pandas, Matplotlib, Astropy, SciPy
- **Astronomy Tools:** astroquery, pyvo, FITS (via astropy.io.fits)
- **Data Archives:** NASA/IPAC IRSA, AllWISE, NEOWISE

---

## Related Publication

Adams, N. (2nd author), Dai, X., Kovacevic, N., et al.
"A Decade-Long Increasing Mid-Infrared Luminosity in Galaxy 
NGC 6447: a Turning-On Candidate of Active Galactic Nucleus"
*Submitted to The Astrophysical Journal*, February 2026
[arXiv:2602.21502](https://arxiv.org/abs/2602.21502)
