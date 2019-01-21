## Lighting in Renderman

#### using the python api

---

## Renderman Light Models

- Lighting in renderman is designed to be simple and flexible
- Most lights are based on simple geometric shapes such as
  - DomeLight, DistantLight, RectLight and SphereLight
- arbitrary geometry may also have a light Bxdf attached to create more complex lighting 

+++

## Lighting A Scene

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



