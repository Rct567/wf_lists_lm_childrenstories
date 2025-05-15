# Word frequency lists based on AI generated children's stories

This repository contains **word frequency lists** based on AI generated children's stories, and the code to generate them.

## How to use

- Create a .env file based on the .env.example file.
- (Optional) Run `generate_titles.py` to generate titles for the stories.
- Run `generate_stories.py` to generate the stories.
- (Optional) Download [stories.zip](https://github.com/Rct567/wf_lists_lm_childrenstories/releases) to get the stories currently used.
- Run `generate_wf_lists.py` to generate the word frequencies lists.

## Word frequency lists overview

| Language | Word count | Story count |
| --- | --- | --- |
| [English](wf_lists/wf_list_en.csv) | 22,500 | 4,000 |
| [Chinese](wf_lists/wf_list_zh.csv) | 26,402 | 3,728 |
| [Russian](wf_lists/wf_list_ru.csv) | 49,255 | 3,727 |
| [Spanish](wf_lists/wf_list_es.csv) | 26,506 | 3,723 |
| [Japanese](wf_lists/wf_list_ja.csv) | 15,829 | 3,721 |
| [Arabic](wf_lists/wf_list_ar.csv) | 64,348 | 3,588 |
| [German](wf_lists/wf_list_de.csv) | 27,592 | 3,269 |
| [Italian](wf_lists/wf_list_it.csv) | 27,568 | 3,267 |
| [Portuguese (Portugal)](wf_lists/wf_list_pt.csv) | 25,932 | 3,262 |
| [French](wf_lists/wf_list_fr.csv) | 27,124 | 3,261 |
| [Dutch](wf_lists/wf_list_nl.csv) | 19,967 | 2,683 |
| [Hungarian](wf_lists/wf_list_hu.csv) | 35,454 | 1,824 |
| [Persian](wf_lists/wf_list_fa.csv) | 12,766 | 1,821 |
| [Danish](wf_lists/wf_list_da.csv) | 15,988 | 1,820 |
| [Greek (Modern)](wf_lists/wf_list_el.csv) | 20,040 | 1,817 |
| [Portuguese (Brazil)](wf_lists/wf_list_pt_br.csv) | 18,460 | 1,817 |
| [Vietnamese](wf_lists/wf_list_vi.csv) | 4,107 | 1,817 |
| [Swedish](wf_lists/wf_list_sv.csv) | 16,534 | 1,816 |
| [Indonesian](wf_lists/wf_list_id.csv) | 10,540 | 1,815 |
| [Thai](wf_lists/wf_list_th.csv) | 9,059 | 1,814 |
| [Polish](wf_lists/wf_list_pl.csv) | 33,262 | 1,813 |
| [Korean](wf_lists/wf_list_ko.csv) | 34,302 | 1,807 |
| [Turkish](wf_lists/wf_list_tr.csv) | 32,062 | 1,805 |
| [Finnish](wf_lists/wf_list_fi.csv) | 32,153 | 1,796 |
| [Norwegian](wf_lists/wf_list_no.csv) | 12,368 | 1,250 |
| [Welsh](wf_lists/wf_list_cy.csv) | 12,348 | 1,242 |
| [Hebrew](wf_lists/wf_list_he.csv) | 20,671 | 1,242 |
| [Armenian](wf_lists/wf_list_hy.csv) | 15,054 | 1,242 |
| [Hindi](wf_lists/wf_list_hi.csv) | 1,472 | 1,240 |
| [Latvian](wf_lists/wf_list_lv.csv) | 21,714 | 1,240 |
| [Norwegian Nynorsk](wf_lists/wf_list_nn.csv) | 13,376 | 1,240 |
| [Catalan](wf_lists/wf_list_ca.csv) | 15,266 | 1,239 |
| [Icelandic](wf_lists/wf_list_is.csv) | 17,478 | 1,239 |
| [Khmer](wf_lists/wf_list_km.csv) | 5,210 | 1,238 |
| [Macedonian](wf_lists/wf_list_mk.csv) | 17,163 | 1,080 |
| [Bulgarian](wf_lists/wf_list_bg.csv) | 19,125 | 1,077 |
| [Galician](wf_lists/wf_list_gl.csv) | 16,042 | 1,077 |
| [Bosnian](wf_lists/wf_list_bs.csv) | 21,076 | 1,074 |
| [Afrikaans](wf_lists/wf_list_af.csv) | 10,084 | 1,073 |
| [Esperanto](wf_lists/wf_list_eo.csv) | 13,904 | 1,073 |
| [Western Frisian](wf_lists/wf_list_fy.csv) | 12,359 | 1,072 |
| [Lithuanian](wf_lists/wf_list_lt.csv) | 20,613 | 1,072 |
| [Tagalog](wf_lists/wf_list_tl.csv) | 9,147 | 1,071 |
| [Malayalam](wf_lists/wf_list_ml.csv) | 2,279 | 1,070 |
| [Romanian](wf_lists/wf_list_ro.csv) | 15,526 | 1,069 |
| [Croatian](wf_lists/wf_list_hr.csv) | 20,731 | 1,068 |
| [Romansh](wf_lists/wf_list_rm.csv) | 21,714 | 1,068 |
| [Punjabi](wf_lists/wf_list_pa.csv) | 1,437 | 1,067 |
| [Estonian](wf_lists/wf_list_et.csv) | 19,739 | 1,066 |
| [Slovak](wf_lists/wf_list_sk.csv) | 22,557 | 1,066 |
| [Belarusian](wf_lists/wf_list_be.csv) | 22,557 | 1,065 |
| [Czech](wf_lists/wf_list_cs.csv) | 23,200 | 1,065 |
| [Albanian](wf_lists/wf_list_sq.csv) | 13,293 | 1,065 |
| [Ukrainian](wf_lists/wf_list_uk.csv) | 22,416 | 1,065 |
| [Urdu](wf_lists/wf_list_ur.csv) | 7,123 | 1,062 |
| [Slovenian](wf_lists/wf_list_sl.csv) | 20,225 | 1,060 |
| [Bengali (Bangla script)](wf_lists/wf_list_bn.csv) | 1,734 | 1,059 |
| [Serbian](wf_lists/wf_list_sr.csv) | 26,194 | 1,059 |
| [Amharic](wf_lists/wf_list_am.csv) | 19,148 | 1,058 |
| [Uighur](wf_lists/wf_list_ug.csv) | 17,901 | 1,058 |
| [Georgian](wf_lists/wf_list_ka.csv) | 15,723 | 1,054 |
| [Nepali](wf_lists/wf_list_ne.csv) | 1,999 | 1,051 |
| [Yiddish (Hebrew script)](wf_lists/wf_list_yi.csv) | 10,997 | 1,051 |
| [Tibetan](wf_lists/wf_list_bo.csv) | 7,846 | 1,048 |
| [Sundanese](wf_lists/wf_list_su.csv) | 10,316 | 1,047 |
| [Haitian](wf_lists/wf_list_ht.csv) | 4,064 | 1,046 |
| [Basque](wf_lists/wf_list_eu.csv) | 13,782 | 1,043 |
| [Mongolian](wf_lists/wf_list_mn.csv) | 15,009 | 1,033 |
| [Latin](wf_lists/wf_list_la.csv) | 17,396 | 1,029 |
| [Lao](wf_lists/wf_list_lo.csv) | 6,859 | 1,022 |
| [Somali](wf_lists/wf_list_so.csv) | 15,935 | 1,005 |
| [Uzbek](wf_lists/wf_list_uz.csv) | 18,189 | 1,005 |
| [Scottish Gaelic](wf_lists/wf_list_gd.csv) | 7,734 | 1,000 |
| [Irish](wf_lists/wf_list_ga.csv) | 9,435 | 992 |
| [Zulu](wf_lists/wf_list_zu.csv) | 27,775 | 976 |
| [Tamil](wf_lists/wf_list_ta.csv) | 1,186 | 961 |
| [Telugu](wf_lists/wf_list_te.csv) | 1,688 | 957 |
| [Kongo](wf_lists/wf_list_kg.csv) | 11,939 | 952 |
| [Old Church Slavonic](wf_lists/wf_list_cu.csv) | 24,402 | 948 |
| [Tatar](wf_lists/wf_list_tt.csv) | 14,230 | 933 |
| [Tajik](wf_lists/wf_list_tg.csv) | 13,165 | 932 |
| [Javanese](wf_lists/wf_list_jv.csv) | 9,374 | 930 |
| [Swahili](wf_lists/wf_list_sw.csv) | 11,316 | 928 |
| [Chechen](wf_lists/wf_list_ce.csv) | 13,143 | 885 |
| [Malagasy](wf_lists/wf_list_mg.csv) | 8,518 | 866 |
| [Breton](wf_lists/wf_list_br.csv) | 2,390 | 79 |
| [Malay](wf_lists/wf_list_ms.csv) | 2,623 | 79 |
| [Sinhala](wf_lists/wf_list_si.csv) | 876 | 79 |
| [Kazakh](wf_lists/wf_list_kk.csv) | 3,533 | 77 |