# site/media

Media the build produces itself, because neither the live site nor Etch can give it in a web-ready form. Images never
go here: they are imported from their originals and compressed on the host with the Etch Asset Manager preset
(CLAUDE.md "Fresh install").

- `Riverside-Wharf-hero.mp4`: the hero loop of Home and the Riverside Wharf offerings. Made by Actions > "Hero video"
  (`.github/workflows/video.yml`) from the live `Dream_Website_banner.mp4` (1920x1080, 30 fps, 5.7 Mbps, 10.5 MB):
  H.264 High, CRF 28, 1920x1080, 30 fps, no audio, start-fast (moov first), 6.4 MB (Alex, 2026-10-09: "even the hero
  video is choppy"). Frames compared side by side with the original before choosing CRF 28. To change it, run the
  workflow (input `crf`), compare, and replace this file with the one on the branch `media/hero-video`.
