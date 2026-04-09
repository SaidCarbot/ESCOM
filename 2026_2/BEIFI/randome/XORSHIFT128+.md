{\rtf1\ansi\ansicpg1252\cocoartf2869
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Demonstration: Planar Structures in xorshift128+\
\
This experiment reproduces a phenomenon reported in the literature, where consecutive outputs of the **xorshift128+** generator exhibit non-uniform structures in three-dimensional space. In particular, consecutive triples `(x, y, z)` tend to concentrate on a small number of planes, contradicting the expected behavior of an ideal pseudo-random number generator.\
\
---\
\
## Code Execution\
\
The code can be executed in the following ways:\
\
### Local Execution\
\
1. Open :contentReference[oaicite:0]\{index=0\}.\
2. Create a script file with `.m` extension (e.g., `xorshift_planes.m`).\
3. Copy and paste the full code into the file.\
4. Run the script from the environment.\
\
### Online Execution\
\
1. Go to https://matlab.mathworks.com  \
2. Sign in with a MathWorks account (institutional or personal).\
3. Create a new script.\
4. Paste the code and run it.\
\
---\
\
## MATLAB Version Compatibility\
\
MATLAB follows a biannual release cycle (versions labeled `RYYYYa` and `RYYYYb`). :contentReference[oaicite:1]\{index=1\}  \
\
The most recent stable versions at the time of writing are:\
\
- R2025b (latest stable release)\
- R2025a\
- R2024b\
- R2024a\
\
MATLAB releases are generally backward compatible across several versions, and typical tooling supports multiple recent releases simultaneously. :contentReference[oaicite:2]\{index=2\}  \
\
### Recommendation\
\
- This script is expected to run without modification on:\
  - R2023a or newer\
- For long-term reproducibility:\
  - Prefer using R2024a\'96R2025b\
- Future versions (e.g., R2026a and beyond) are expected to remain compatible, as the code relies only on core language features (`uint64`, `bitxor`, `bitshift`, `scatter3`), which are stable across releases.\
\
---\
\
## Generator Parameters\
\
```matlab\
a = 5;\
b = 17;\
c = 26;}