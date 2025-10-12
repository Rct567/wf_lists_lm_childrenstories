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
| [English](wf_lists/wf_list_en.csv) | 24,173 | 4,460 |
| [Chinese](wf_lists/wf_list_zh.csv) | 29,484 | 4,179 |
| [Spanish](wf_lists/wf_list_es.csv) | 29,649 | 4,176 |
| [Russian](wf_lists/wf_list_ru.csv) | 54,812 | 4,152 |
| [Japanese](wf_lists/wf_list_ja.csv) | 17,396 | 4,149 |
| [Arabic](wf_lists/wf_list_ar.csv) | 75,790 | 4,035 |
| [German](wf_lists/wf_list_de.csv) | 31,780 | 3,735 |
| [Italian](wf_lists/wf_list_it.csv) | 30,985 | 3,733 |
| [Portuguese (Portugal)](wf_lists/wf_list_pt.csv) | 29,394 | 3,730 |
| [French](wf_lists/wf_list_fr.csv) | 30,601 | 3,726 |
| [Dutch](wf_lists/wf_list_nl.csv) | 24,047 | 3,456 |
| [Persian](wf_lists/wf_list_fa.csv) | 16,236 | 2,759 |
| [Portuguese (Brazil)](wf_lists/wf_list_pt_br.csv) | 23,646 | 2,759 |
| [Greek (Modern)](wf_lists/wf_list_el.csv) | 26,272 | 2,756 |
| [Polish](wf_lists/wf_list_pl.csv) | 45,445 | 2,755 |
| [Danish](wf_lists/wf_list_da.csv) | 21,640 | 2,753 |
| [Indonesian](wf_lists/wf_list_id.csv) | 13,089 | 2,753 |
| [Hungarian](wf_lists/wf_list_hu.csv) | 51,458 | 2,751 |
| [Swedish](wf_lists/wf_list_sv.csv) | 22,077 | 2,749 |
| [Vietnamese](wf_lists/wf_list_vi.csv) | 4,496 | 2,749 |
| [Korean](wf_lists/wf_list_ko.csv) | 49,658 | 2,728 |
| [Thai](wf_lists/wf_list_th.csv) | 11,327 | 2,728 |
| [Turkish](wf_lists/wf_list_tr.csv) | 44,870 | 2,717 |
| [Finnish](wf_lists/wf_list_fi.csv) | 45,108 | 2,707 |
| [Norwegian Bokmål](wf_lists/wf_list_nb.csv) | 20,345 | 2,592 |
| [Hebrew](wf_lists/wf_list_he.csv) | 33,999 | 2,579 |
| [Icelandic](wf_lists/wf_list_is.csv) | 31,003 | 2,572 |
| [Catalan](wf_lists/wf_list_ca.csv) | 25,455 | 2,569 |
| [Latvian](wf_lists/wf_list_lv.csv) | 37,660 | 2,547 |
| [Galician](wf_lists/wf_list_gl.csv) | 27,842 | 2,419 |
| [Macedonian](wf_lists/wf_list_mk.csv) | 29,542 | 2,409 |
| [Bulgarian](wf_lists/wf_list_bg.csv) | 32,796 | 2,402 |
| [Ukrainian](wf_lists/wf_list_uk.csv) | 41,399 | 2,399 |
| [Albanian](wf_lists/wf_list_sq.csv) | 23,068 | 2,397 |
| [Tagalog](wf_lists/wf_list_tl.csv) | 15,565 | 2,397 |
| [Bosnian](wf_lists/wf_list_bs.csv) | 37,019 | 2,395 |
| [Croatian](wf_lists/wf_list_hr.csv) | 37,474 | 2,390 |
| [Slovak](wf_lists/wf_list_sk.csv) | 41,985 | 2,388 |
| [Romanian](wf_lists/wf_list_ro.csv) | 26,335 | 2,386 |
| [Urdu](wf_lists/wf_list_ur.csv) | 10,579 | 2,386 |
| [Esperanto](wf_lists/wf_list_eo.csv) | 25,845 | 2,384 |
| [Czech](wf_lists/wf_list_cs.csv) | 42,644 | 2,382 |
| [Slovenian](wf_lists/wf_list_sl.csv) | 37,228 | 2,378 |
| [Serbian](wf_lists/wf_list_sr.csv) | 50,624 | 2,376 |
| [Estonian](wf_lists/wf_list_et.csv) | 37,029 | 2,375 |
| [Lithuanian](wf_lists/wf_list_lt.csv) | 39,334 | 2,375 |
| [Basque](wf_lists/wf_list_eu.csv) | 24,931 | 2,358 |
| [Georgian](wf_lists/wf_list_ka.csv) | 32,723 | 2,358 |
| [Malay](wf_lists/wf_list_ms.csv) | 12,691 | 2,331 |
| [Hindi](wf_lists/wf_list_hi.csv) | 1,663 | 1,745 |
| [Armenian](wf_lists/wf_list_hy.csv) | 18,454 | 1,740 |
| [Malayalam](wf_lists/wf_list_ml.csv) | 2,628 | 1,575 |
| [Afrikaans](wf_lists/wf_list_af.csv) | 12,599 | 1,573 |
| [Bengali (Bangla script)](wf_lists/wf_list_bn.csv) | 2,081 | 1,568 |
| [Breton](wf_lists/wf_list_br.csv) | 15,369 | 1,535 |
| [Tamil](wf_lists/wf_list_ta.csv) | 1,322 | 1,510 |
| [Telugu](wf_lists/wf_list_te.csv) | 1,986 | 1,508 |
| [Sinhala](wf_lists/wf_list_si.csv) | 2,626 | 1,504 |
| [Kazakh](wf_lists/wf_list_kk.csv) | 22,349 | 1,494 |
| [Welsh](wf_lists/wf_list_cy.csv) | 12,594 | 1,262 |
| [Norwegian Nynorsk](wf_lists/wf_list_nn.csv) | 13,599 | 1,259 |
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