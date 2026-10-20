"""Concept markup for the Zisel print business cards. Edit text/colors here, then run build.py."""
LOGO = ('<div class="logo{cls}" style="--ls:{ls}px"><div class="word">Z<span class="i">ı<img class="gem" src="gem.svg"></span>sel</div>'
        '<div class="jw {jw}">JEWELRY</div></div>')
NAME, BIZ, TAG, PHONE, LOC = ("Jonathan Shulkin", "ZISEL JEWELRY", "Wholesale Diamond &amp; Fine Jewelry", "725.254.6937", "Las Vegas, Nevada")

def back_stack(name_c, biz_c, tag_c, rule_bg, phone_c, loc_c, align="center", extra=""):
    return (f'<div class="content" style="{extra}align-items:{align};text-align:{"left" if align=="flex-start" else "center"}">'
            f'<div class="name {name_c[0]}" style="color:{name_c[1]}">{NAME}</div>'
            f'<div class="biz {biz_c[0]}" style="color:{biz_c[1]}">{BIZ}</div>'
            f'<div class="tag" style="color:{tag_c}">{TAG}</div>'
            f'<div class="rule" style="background:{rule_bg}"></div>'
            f'<div class="phone {phone_c[0]}" style="color:{phone_c[1]}">{PHONE}</div>'
            f'<div class="loc" style="color:{loc_c}">{LOC}</div></div>')

CONCEPTS = {
 "A": dict(title="A · Gold Frame Classic",
   desc="Navy front with the logo and a fine gold hairline frame; white back with navy name, deep-gold accents and the same hairline.",
   front='<div class="card navy"><div class="hair"></div><div class="content">' + LOGO.format(cls="", ls=54, jw="goldtext") + '</div></div>',
   back='<div class="card paper"><div class="hair"></div>' + back_stack(("", "#0d1f45"), ("golddeep", ""), "#3a4a6b", "#a7802d", ("", "#0d1f45"), "#5a6684") + '</div>'),
 "B": dict(title="B · Midnight",
   desc="Navy on both sides, no frame. Front: logo only. Back: left-aligned gold name and phone with white supporting lines and a small gold rule.",
   front='<div class="card navy"><div class="content">' + LOGO.format(cls="", ls=58, jw="goldtext") + '</div></div>',
   back='<div class="card flatnavy">' + back_stack(("goldtext", ""), ("", "#ffffff"), "#dfe6f5", "#c99a3a", ("goldtext", ""), "#c9d3ea", align="flex-start", extra="padding-left:.14in;") + '</div>'),
 "C": dict(title="C · Ivory & Midnight",
   desc="White front with the navy-and-gold logo floating on paper; navy back with centered white name, gold accents and a gold hairline frame.",
   front='<div class="card paper"><div class="content">' + LOGO.format(cls=" onwhite", ls=54, jw="golddeep") + '</div></div>',
   back='<div class="card navy"><div class="hair" style="border-color:#d8b35a"></div>' + back_stack(("", "#ffffff"), ("goldtext", ""), "#dfe6f5", "#c99a3a", ("goldtext", ""), "#c9d3ea") + '</div>'),
}
