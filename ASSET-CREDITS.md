# Asset provenance / 素材来源

The packaged Remotion project has five museum reproductions, five AI-generated scene paintings, and eight motion plates derived from those paintings. It does not include the original personal music, copied font binaries, or the OpenAI logo vector.

公开工程收录五幅名画复制图、五幅 AI 生成场景和八张根据场景制作的运动切图；不收录原片个人音乐、复制字体或 OpenAI 标志矢量。

| File in `public/art/` | Source | Status stated by source |
| --- | --- | --- |
| `cypresses.jpg` | [The Met, object 436535](https://www.metmuseum.org/art/collection/search/436535) | Open Access / CC0 |
| `pitcher.jpg` | [The Met, object 437881](https://www.metmuseum.org/art/collection/search/437881) | Open Access / CC0 |
| `wave-met.jpg` | [The Met, object 39799](https://www.metmuseum.org/art/collection/search/39799) | Open Access / CC0 |
| `boating.jpg` | [The Met, object 436947](https://www.metmuseum.org/art/collection/search/436947) | Open Access / CC0 |
| `pearl.jpg` | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Girl_with_a_Pearl_Earring.jpg) | Public domain mark |

The Met's [Open Access policy](https://www.metmuseum.org/policies/image-resources) describes reuse of its public-domain images. `library.jpg`, `city.jpg`, `dawn.jpg`, `observatory.jpg`, and `mountains.jpg` were generated for the original film; their prompts are in `assets-generation.json` inside the archive. `public/motion-assets/` contains subsequent edits and cutouts. The archive's `art-sources.json` carries the individual artwork source URLs.

The [MIT License](LICENSE) covers the author's skill text, scripts, reference project source code, and AI-generated scenes and motion plates to the extent the author can license them. Public-domain museum images retain their source status. Remotion and npm dependencies are installed separately and follow their own licenses. Generated images may not receive identical copyright treatment in every jurisdiction.
