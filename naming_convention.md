# Simulation naming convention

The convention is

`Xj_Yj_Ss_Aa_Ppe`

where
- X = mass of inner planet
- Y = mass of outer planet
- S = factor to multiply default surface density $\Sigma_0$ by
- A = power to raise 10 to to get the alpha viscosity
- P = factor to multiply default photoevaporation rate by


## Examples

`2j_1j_1s_3a_0pe`
- inner planet has mass $2M_{Jup}$
- outer planet has mass $1M_{Jup}$
- $\Sigma_0$ is the default
- $\alpha = 10^{-3}$
- no photoevaporation

`2j_2j_4s_3a_2pe`
- both planets have mass $2M_{Jup}$
- $\Sigma_0$ is 4x the default
- $\alpha = 10^{-4}$
- 2x photoevaporation rate