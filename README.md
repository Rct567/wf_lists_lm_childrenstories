# Word frequency lists based on AI generated children's stories

This repository contains **word frequency lists** based on AI generated children's stories, and the code to generate them.

## How to use

- Create a .env file based on the .env.example file.
- (Optional) Run `generate_titles.py` to generate titles for the stories.
- Run `generate_stories.py` to generate the stories.
- (Optional) Download [stories.zip](https://github.com/Rct567/wf_lists_lm_childrenstories/releases) to get the generated stories currently used.
- Run `generate_wf_lists.py` to generate the word frequencies lists.

## Word frequency lists overview


| Language | Word count | Story count |
| --- | --- | --- |
| [English](wf_lists/wf_list_en.csv) | 24,428 | 4,559 |
| [French](wf_lists/wf_list_fr.csv) | 33,440 | 4,278 |
| [Spanish](wf_lists/wf_list_es.csv) | 30,053 | 4,274 |
| [Chinese](wf_lists/wf_list_zh.csv) | 29,872 | 4,274 |
| [Russian](wf_lists/wf_list_ru.csv) | 55,793 | 4,248 |
| [Japanese](wf_lists/wf_list_ja.csv) | 17,567 | 4,238 |
| [Arabic](wf_lists/wf_list_ar.csv) | 77,810 | 4,130 |
| [Portuguese (Portugal)](wf_lists/wf_list_pt.csv) | 29,871 | 3,828 |
| [German](wf_lists/wf_list_de.csv) | 32,417 | 3,827 |
| [Italian](wf_lists/wf_list_it.csv) | 31,497 | 3,827 |
| [Dutch](wf_lists/wf_list_nl.csv) | 24,166 | 3,483 |
| [Portuguese (Brazil)](wf_lists/wf_list_pt_br.csv) | 23,820 | 2,791 |
| [Persian](wf_lists/wf_list_fa.csv) | 16,357 | 2,789 |
| [Greek (Modern)](wf_lists/wf_list_el.csv) | 26,467 | 2,788 |
| [Indonesian](wf_lists/wf_list_id.csv) | 13,176 | 2,788 |
| [Polish](wf_lists/wf_list_pl.csv) | 45,867 | 2,787 |
| [Danish](wf_lists/wf_list_da.csv) | 21,853 | 2,784 |
| [Swedish](wf_lists/wf_list_sv.csv) | 22,269 | 2,782 |
| [Hungarian](wf_lists/wf_list_hu.csv) | 51,979 | 2,780 |
| [Vietnamese](wf_lists/wf_list_vi.csv) | 4,509 | 2,780 |
| [Korean](wf_lists/wf_list_ko.csv) | 50,154 | 2,758 |
| [Thai](wf_lists/wf_list_th.csv) | 11,382 | 2,752 |
| [Turkish](wf_lists/wf_list_tr.csv) | 45,303 | 2,745 |
| [Finnish](wf_lists/wf_list_fi.csv) | 45,577 | 2,738 |
| [Norwegian Bokmål](wf_lists/wf_list_nb.csv) | 20,501 | 2,625 |
| [Hebrew](wf_lists/wf_list_he.csv) | 34,177 | 2,610 |
| [Icelandic](wf_lists/wf_list_is.csv) | 31,311 | 2,604 |
| [Catalan](wf_lists/wf_list_ca.csv) | 25,691 | 2,600 |
| [Latvian](wf_lists/wf_list_lv.csv) | 38,034 | 2,578 |
| [Galician](wf_lists/wf_list_gl.csv) | 28,089 | 2,452 |
| [Macedonian](wf_lists/wf_list_mk.csv) | 29,790 | 2,440 |
| [Bulgarian](wf_lists/wf_list_bg.csv) | 33,146 | 2,438 |
| [Albanian](wf_lists/wf_list_sq.csv) | 23,329 | 2,433 |
| [Tagalog](wf_lists/wf_list_tl.csv) | 15,679 | 2,430 |
| [Ukrainian](wf_lists/wf_list_uk.csv) | 41,852 | 2,430 |
| [Bosnian](wf_lists/wf_list_bs.csv) | 37,297 | 2,424 |
| [Croatian](wf_lists/wf_list_hr.csv) | 37,785 | 2,421 |
| [Romanian](wf_lists/wf_list_ro.csv) | 26,560 | 2,420 |
| [Slovak](wf_lists/wf_list_sk.csv) | 42,525 | 2,419 |
| [Urdu](wf_lists/wf_list_ur.csv) | 10,660 | 2,418 |
| [Czech](wf_lists/wf_list_cs.csv) | 43,116 | 2,416 |
| [Esperanto](wf_lists/wf_list_eo.csv) | 26,077 | 2,416 |
| [Slovenian](wf_lists/wf_list_sl.csv) | 37,599 | 2,410 |
| [Serbian](wf_lists/wf_list_sr.csv) | 51,137 | 2,407 |
| [Estonian](wf_lists/wf_list_et.csv) | 37,407 | 2,406 |
| [Lithuanian](wf_lists/wf_list_lt.csv) | 39,742 | 2,404 |
| [Georgian](wf_lists/wf_list_ka.csv) | 33,137 | 2,390 |
| [Basque](wf_lists/wf_list_eu.csv) | 25,240 | 2,388 |
| [Malay](wf_lists/wf_list_ms.csv) | 12,761 | 2,364 |
| [Armenian](wf_lists/wf_list_hy.csv) | 19,613 | 1,845 |
| [Hindi](wf_lists/wf_list_hi.csv) | 1,663 | 1,745 |
| [Malayalam](wf_lists/wf_list_ml.csv) | 2,730 | 1,679 |
| [Afrikaans](wf_lists/wf_list_af.csv) | 13,336 | 1,677 |
| [Breton](wf_lists/wf_list_br.csv) | 16,270 | 1,635 |
| [Sinhala](wf_lists/wf_list_si.csv) | 2,722 | 1,601 |
| [Kazakh](wf_lists/wf_list_kk.csv) | 23,842 | 1,594 |
| [Bengali (Bangla script)](wf_lists/wf_list_bn.csv) | 2,081 | 1,568 |
| [Tamil](wf_lists/wf_list_ta.csv) | 1,322 | 1,510 |
| [Telugu](wf_lists/wf_list_te.csv) | 1,986 | 1,508 |
| [Norwegian Nynorsk](wf_lists/wf_list_nn.csv) | 13,774 | 1,272 |
| [Welsh](wf_lists/wf_list_cy.csv) | 12,594 | 1,262 |
| [Khmer](wf_lists/wf_list_km.csv) | 5,288 | 1,258 |
| [Western Frisian](wf_lists/wf_list_fy.csv) | 12,717 | 1,096 |
| [Punjabi](wf_lists/wf_list_pa.csv) | 1,457 | 1,087 |
| [Romansh](wf_lists/wf_list_rm.csv) | 22,251 | 1,086 |
| [Belarusian](wf_lists/wf_list_be.csv) | 23,131 | 1,084 |
| [Amharic](wf_lists/wf_list_am.csv) | 19,954 | 1,080 |
| [Uighur](wf_lists/wf_list_ug.csv) | 18,498 | 1,080 |
| [Nepali](wf_lists/wf_list_ne.csv) | 2,023 | 1,073 |
| [Yiddish (Hebrew script)](wf_lists/wf_list_yi.csv) | 11,421 | 1,071 |
| [Tibetan](wf_lists/wf_list_bo.csv) | 8,006 | 1,069 |
| [Sundanese](wf_lists/wf_list_su.csv) | 10,589 | 1,068 |
| [Haitian](wf_lists/wf_list_ht.csv) | 4,118 | 1,066 |
| [Mongolian](wf_lists/wf_list_mn.csv) | 15,411 | 1,055 |
| [Latin](wf_lists/wf_list_la.csv) | 17,776 | 1,045 |
| [Lao](wf_lists/wf_list_lo.csv) | 7,083 | 1,045 |
| [Somali](wf_lists/wf_list_so.csv) | 16,551 | 1,030 |
| [Uzbek](wf_lists/wf_list_uz.csv) | 18,688 | 1,024 |
| [Scottish Gaelic](wf_lists/wf_list_gd.csv) | 7,922 | 1,022 |
| [Irish](wf_lists/wf_list_ga.csv) | 9,777 | 1,021 |
| [Zulu](wf_lists/wf_list_zu.csv) | 29,894 | 1,021 |
| [Kongo](wf_lists/wf_list_kg.csv) | 13,031 | 993 |
| [Old Church Slavonic](wf_lists/wf_list_cu.csv) | 26,413 | 992 |
| [Tajik](wf_lists/wf_list_tg.csv) | 13,887 | 973 |
| [Tatar](wf_lists/wf_list_tt.csv) | 15,160 | 972 |
| [Javanese](wf_lists/wf_list_jv.csv) | 9,721 | 969 |
| [Swahili](wf_lists/wf_list_sw.csv) | 12,059 | 968 |
| [Malagasy](wf_lists/wf_list_mg.csv) | 9,055 | 910 |
| [Chechen](wf_lists/wf_list_ce.csv) | 14,056 | 902 |