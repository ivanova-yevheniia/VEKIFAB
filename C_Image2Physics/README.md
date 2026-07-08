in World sind die .spz dateien die Scaniverse dateien, welche in drei Qualitätsstufen (100k - 500k) vorhanden sind.

Um gaussianSplat in Unity zu starten, muss die Datei "UnityGaussianSplatting\projects\GaussianExample\Assets\GSTestScene.unity"  in Unity gestartet werden, dann 

Next up, **create some GaussianSplat assets**: open `Tools -> Gaussian Splats -> Create GaussianSplatAsset` menu within Unity. In the dialog, point `Input PLY/SPZ File` to your Gaussian Splat file. Currently two file formats are supported:

* PLY format from the original 3DGS paper (in the official paper models, the correct files are under `point_cloud/iteration_*/point_cloud.ply`).
* [Scaniverse SPZ](https://scaniverse.com/spz) format.



UnityGaussianSplat hier holen: "[aras-p/UnityGaussianSplatting: Toy Gaussian Splatting visualization in Unity](https://github.com/aras-p/UnityGaussianSplatting)"
