## Lighting in Renderman

#### using the python api

---

## Renderman Light Models

- Lighting in renderman is designed to be simple and flexible
- Most lights are based on simple geometric shapes such as
  - DomeLight, DistantLight, RectLight and SphereLight
- arbitrary geometry may also have a light Bxdf attached to create more complex lighting 

+++

## [Lighting A Scene](https://rmanwiki.pixar.com/display/REN22/Lighting)

- There are 3 ways to light a scene
  - Analytic Lights 
  - Mesh Lights 
  - Emissive Surfaces

+++

## Analytic Lights

-  These are the preferred choice. 
- These provide superior memory usage, flexibility, and speed. 
- Their visibility is a simple on and off for camera visibility.
- PxrDomeLight - The domelight acts as the environment light for a scene and is often mapped with a high dymanic range image (HDRI).
  - ```PxrRectLight PxrDistantLight PxrDiskLight PxrSphereLight PxrEnvDaylight PxrPortalLight , PxrDomeLight``` 

+++

## Mesh Lights 

- These are great for using arbitrary shapes in lighting. 
- These consume more memory since they are geometry and complex shapes may increase noise. 
- These can make use of visibility like any other object: camera, shadow/transmission, and indirect visibility.
  - ```PxrMeshLight ```

+++

## Emissive Surfaces 
 - These typically use a constant bxdf or "glow" parameter to light a scene indirectly. 
 - This is inefficient and should usually be avoided but may be useful for texture mapping "lights" onto futuristic objects and panels!


--

## References

- [Lighting](https://rmanwiki.pixar.com/display/REN22/Lighting)