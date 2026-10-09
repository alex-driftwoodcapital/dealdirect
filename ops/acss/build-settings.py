#!/usr/bin/env python3
"""Build ops/acss/dealdirect-settings.json: the ACSS 4.0.1 dashboard INPUT keys for DealDirect.
Source of every value: handoff/docs/acss-mapping.md + handoff/README.md (design tokens).
Only input keys are written; ACSS derives everything else when it regenerates.
Shade overrides are stored the way ACSS 4.0.1 stores them: <color>-<shade>-{l,c,h}-oklch (key names
taken from the 4.0.1 export in .claude/skills/acss-expert/index/acss-settings.json).
usage: python3 -I ops/acss/build-settings.py   (writes the JSON next to this script)"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))

def oklch(hex_):
    """sRGB hex -> (L 0..1, C, H degrees), Björn Ottosson's OKLab."""
    r, g, b = (int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    C = math.hypot(A, B)
    H = math.degrees(math.atan2(B, A)) % 360
    return round(L, 3), round(C, 3), round(H, 2)

# Base colours (Dashboard > Color)
COLORS = {
    'primary': '#0B2B48',    # navy ink-800
    'secondary': '#2468A8',  # ocean
    'accent': '#6FB0E0',     # teal-soft, on dark only
    'tertiary': '#00AFA0',   # brand teal, logo only
    'base': '#F5F6F8',       # slate-50
    'neutral': '#A9B2BE',    # slate-300
}
# Shade overrides from acss-mapping.md
SHADES = {
    'primary': {'ultra-dark': '#061A2E', 'dark': '#061A2E', 'semi-dark': '#14385B', 'hover': '#14385B', 'semi-light': '#22527F', 'light': '#3A6E9E'},
    'secondary': {'dark': '#1B5388', 'hover': '#2060A0', 'light': '#5C97C9', 'ultra-light': '#B6D5EC'},
    'base': {'ultra-light': '#FFFFFF', 'light': '#E9ECF0', 'semi-light': '#D3D8E0', 'semi-dark': '#4A5564', 'dark': '#2E3744', 'ultra-dark': '#1C2430'},
}

s = {}
for name, hx in COLORS.items():
    # ACSS 4.0.1 builds each colour from <color>-{l,c,h}-oklch; color-<name> (hex) is only what the dashboard shows,
    # so writing it alone left staging on the previous build's palette (teal --primary, QA 2026-10-09).
    s[f'color-{name}'] = hx
    s[f'{name}-l-oklch'], s[f'{name}-c-oklch'], s[f'{name}-h-oklch'] = oklch(hx)
    s[f'option-{name}-clr'] = 'on'
for name, shades in SHADES.items():
    for shade, hx in shades.items():
        L, C, H = oklch(hx)
        s[f'{name}-{shade}-l-oklch'], s[f'{name}-{shade}-c-oklch'], s[f'{name}-{shade}-h-oklch'] = L, C, H

s.update({
    'website-color-scheme': 'light only',
    # Typography: Plus Jakarta Sans variable (OFL), self-hosted: the latin subset (covers the EN/ES/PT copy) ships with
    # dealdirect-core, so the same file is on staging and live. Site-root path: works on any host.
    'font-1-family-name': 'Plus Jakarta Sans', 'font-1-type': 'variable', 'font-1-weight': '200 800',
    'font-1-style': 'normal', 'font-1-display': 'swap', 'font-1-format': 'woff2',
    'font-1-src': '/wp-content/plugins/dealdirect-core/assets/fonts/plus-jakarta-sans-latin-wght-normal.woff2',
    'font-2-family-name': '', 'font-2-src': '',
    'text-font-family': '"Plus Jakarta Sans", system-ui, sans-serif',
    'heading-font-family': '"Plus Jakarta Sans", system-ui, sans-serif',
    'heading-weight': '300',
    'heading-letter-spacing': '-0.034em',
    'h1-line-height': '1.06', 'h2-line-height': '1.06',
    'heading-color': 'var(--primary-ultra-dark)',
    'body-color': '#48535F',
    'body-bg-color': 'var(--white)',
    # Type scale, desktop max / mobile min (px), from the designs' sizes. Page CSS uses only these tokens
    # (var(--h2), var(--text-m)...); site/build.py refuses literal font sizes. h2 = the section titles (28-46),
    # text-xxl = the big stat figures (28-38), text-xl = card titles and big ledes (18-23).
    'h1-max': 88, 'h1-min': 42, 'h2-max': 46, 'h2-min': 28, 'h3-max': 32, 'h3-min': 24, 'h4-max': 18, 'h4-min': 17,
    'text-xxl-max': 38, 'text-xxl-min': 28, 'text-xl-max': 23, 'text-xl-min': 18,
    'text-l-max': 20, 'text-l-min': 16, 'text-m-max': 16, 'text-m-min': 15, 'text-s-max': 14, 'text-s-min': 14,
    'text-xs-max': 12, 'text-xs-min': 12,
    # Layout: content width 1334, gutter 32 desktop
    'vp-max': '1334', 'vp-min': 360, 'gutter-max': 32, 'gutter-min': 16,
    # Radius: 12 buttons/base; 24/20/10 are custom props in the custom CSS step
    'base-radius': '12px', 'btn-border-radius': '12px',
    # Buttons: 52px tall = 12px x 1.333 line-height + 2 x 17px padding + 2 x 1px border; 12px / 700 / .13em uppercase
    'btn-font-size': '0.75rem', 'btn-font-weight': '700', 'btn-letter-spacing': '0.13em', 'btn-text-transform': 'uppercase',
    'btn-padding-block': '17px', 'btn-padding-inline': '28px', 'btn-line-height': '1.333', 'btn-border-width': '1px',
    # Links + focus
    'link-color': 'var(--secondary)', 'link-color-hover': 'var(--secondary-dark)',
    'focus-color': 'var(--secondary)',
    'bg-dark-focus-color': 'var(--white)', 'bg-ultra-dark-focus-color': 'var(--white)',
})

out = os.path.join(HERE, 'dealdirect-settings.json')
with open(out, 'w') as f:
    json.dump(dict(sorted(s.items())), f, indent=1)
    f.write('\n')
print(f'{len(s)} keys -> {out}')
