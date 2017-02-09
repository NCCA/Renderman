/*  $Date: 2015/04/23 $  $Revision: #1 $
# ------------------------------------------------------------------------------
#
# Copyright (c) 2014 Pixar Animation Studios. All rights reserved.
#
# The information in this file (the "Software") is provided for the
# exclusive use of the software licensees of Pixar.  Licensees have
# the right to incorporate the Software into other products for use
# by other authorized software licensees of Pixar, without fee.
# Except as expressly permitted herein, the Software may not be
# disclosed to third parties, copied or duplicated in any form, in
# whole or in part, without the prior written permission of
# Pixar Animation Studios.
#
# The copyright notices in the Software and this entire statement,
# including the above license grant, this restriction and the
# following disclaimer, must be included in all copies of the
# Software, in whole or in part, and all permitted derivative works of
# the Software, unless such copies or derivative works are solely
# in the form of machine-executable object code generated by a
# source language processor.
#
# PIXAR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT
# SHALL PIXAR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES
# OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
#
# Pixar
# 1200 Park Ave
# Emeryville CA 94608
#
# ------------------------------------------------------------------------------
*/
#include "RixPattern.h" 
#include "RixShadingUtils.h"

// comment out the OPTIMIZED define to compile the un-optimized version.
#define OPTIMIZED
#define k_max_radius 1.0f
#define k_noise_average 0.5f


class PxrMyFractal : public RixPattern
{
public:

    PxrMyFractal();
    virtual ~PxrMyFractal();

    virtual int Init(RixContext &, char const *pluginpath);
    virtual RixSCParamInfo const *GetParamTable();
    virtual void Finalize(RixContext &);

    virtual int ComputeOutputParams(RixShadingContext const *,
                                    RtInt *noutputs, 
                                    OutputSpec **outputs,
                                    RtConstPointer instanceData,
                                    RixSCParamInfo const *);
private:

    RtInt m_layers;
    RtFloat m_frequency;
    RtFloat m_lacunarity;
    RtFloat m_dimension;
    RtFloat m_erosion;
    RtFloat m_variation;
    RixShadeFunctions *m_sFuncs;

    float smoothNoise (RtPoint3 const &Q, float variation)
    {
        return (RixSmoothStep (.2f, .8f, m_sFuncs->Noise(Q, variation))); 
    }
};

PxrMyFractal::PxrMyFractal() :
    m_layers(6),
    m_frequency(1.0f),
    m_lacunarity(2.0f),
    m_dimension(1.0f),
    m_erosion(0.0f),
    m_variation(0.0f),
    m_sFuncs(NULL)
{
}

PxrMyFractal::~PxrMyFractal()
{
}

int
PxrMyFractal::Init(RixContext &ctx, char const *pluginpath)
{
    m_sFuncs = (RixShadeFunctions*)ctx.GetRixInterface(k_RixShadeFunctions);
    if (!m_sFuncs)
        return 1;
    else
        return 0;
}

enum paramId
{
    k_resultF = 0,
    k_layers,
    k_frequency,
    k_lacunarity,
    k_dimension,
    k_erosion,
    k_variation,
    k_manifoldBegin,
    k_manifoldQ,
    k_manifoldQradius,
    k_manifoldEnd
};

RixSCParamInfo const *
PxrMyFractal::GetParamTable()
{
    static RixSCParamInfo s_ptable[] = 
    {
        RixSCParamInfo("resultF", k_RixSCFloat, k_RixSCOutput),

        RixSCParamInfo("layers", k_RixSCInteger),
        RixSCParamInfo("frequency", k_RixSCFloat),
        RixSCParamInfo("lacunarity", k_RixSCFloat),
        RixSCParamInfo("dimension", k_RixSCFloat),
        RixSCParamInfo("erosion", k_RixSCFloat),
        RixSCParamInfo("variation", k_RixSCFloat),

        RixSCParamInfo("PxrManifold", "manifold", k_RixSCStructBegin),
            RixSCParamInfo("Q", k_RixSCPoint),
            RixSCParamInfo("Qradius", k_RixSCFloat),
        RixSCParamInfo("PxrManifold", "manifold", k_RixSCStructEnd),

        RixSCParamInfo() // end of table
    };
    return &s_ptable[0];
}

void
PxrMyFractal::Finalize(RixContext &ctx)
{
}


int
PxrMyFractal::ComputeOutputParams(RixShadingContext const *sctx,
                                RtInt *noutputs, OutputSpec **outputs,
                                RtConstPointer instanceData,
                                RixSCParamInfo const *ignored)
{
    bool varying = true;
    RtInt const *layers;
    sctx->EvalParam(k_layers, -1, &layers, &m_layers, varying);

    RtFloat const *frequency;
    sctx->EvalParam(k_frequency, -1, &frequency, &m_frequency, varying);

    RtFloat const *lacunarity;
    sctx->EvalParam(k_lacunarity, -1, &lacunarity, &m_lacunarity, varying);

    RtFloat const *dimension;
    sctx->EvalParam(k_dimension, -1, &dimension, &m_dimension, varying);

    RtFloat const *erosion;
    sctx->EvalParam(k_erosion, -1, &erosion, &m_erosion, varying);

    RtFloat const *variation;
    sctx->EvalParam(k_variation, -1, &variation, &m_variation, varying);


    // Allocate and bind our outputs
    RixShadingContext::Allocator pool(sctx);
    OutputSpec *o = pool.AllocForPattern<OutputSpec>(2);
    *outputs = o;
    *noutputs = 1;
    RtFloat *resultF = NULL;

    resultF = pool.AllocForPattern<RtFloat>(sctx->numPts);

    o[0].paramId = k_resultF;
    o[0].detail  = k_RixSCVarying;
    o[0].value = (RtPointer) resultF;

    // check for manifold input
    RixSCType type;    
    RixSCConnectionInfo cinfo;

    RtPoint3 const *Q;
    RtFloat const *Qradius;
    sctx->GetParamInfo(k_manifoldBegin, &type, &cinfo);
    if (cinfo != k_RixSCNetworkValue)
    {
        // We want P by default (not st)
        sctx->GetBuiltinVar(RixShadingContext::k_P, &Q);
        sctx->GetBuiltinVar(RixShadingContext::k_PRadius, &Qradius);
    } 
    else
    {
        RtPoint3 const *mQ;
        RtFloat const *mQradius;
        sctx->EvalParam(k_manifoldQ, -1, &mQ);
        sctx->EvalParam(k_manifoldQradius, -1, &mQradius);
        Q = mQ;
        Qradius = mQradius;
    }

    float sum, mag, f, fradius;
    for (int i=0; i<sctx->numPts; i++)
    {
        f = frequency[i];
        fradius = Qradius[i]*f;

        #ifdef OPTIMIZED
        // if k_max_radius has been reached, return the noise function's 
        // average value.
        if (fradius >= k_max_radius)
        {
            // skip the noise and smoothstep computations.
            resultF[i] = k_noise_average;
        }
        else
        #endif
            resultF[i] = RixMix(smoothNoise(f*Q[i], variation[i]),
                                k_noise_average, RixSmoothStep(.25f, k_max_radius, fradius));
        sum = 1.0f;

        for (int j=1; j < layers[i]; j+=1)
        {
            f *= lacunarity[i];
            fradius = Qradius[i]*f;

            mag = 1.0f/powf(f, 3.0f - 2.0f*dimension[i] +
                            RixMix(-erosion[i], erosion[i], resultF[i]/sum));

            #ifdef OPTIMIZED
            // we still want to accumulate a number of scaled filtered octaves
            // to approach the limit value. We give up when this octave's
            // contribution becomes too small though : 0.01*0.5 = 0.005
            if (mag < 0.01f)
                break;
            #endif

            #ifdef OPTIMIZED
            // if k_max_radius has been reached, return the noise function's 
            // average value.
            if (fradius >= k_max_radius)
            {
                // skip the noise and smoothstep computations.
                resultF[i] += mag * k_noise_average;
            }
            else
            #endif
                resultF[i] += mag *
                              RixMix(smoothNoise(f*Q[i], variation[i]), 
                                     k_noise_average,
                                     RixSmoothStep (.25f, k_max_radius, fradius));
            sum += mag;
        }

        resultF[i] =static_cast <float> (rand()) / static_cast <float> (RAND_MAX);///= sum;
    }

    return 0;
}

RIX_PATTERNCREATE
{
    return new PxrMyFractal();
}

RIX_PATTERNDESTROY
{
    delete ((PxrMyFractal*)pattern);
}

