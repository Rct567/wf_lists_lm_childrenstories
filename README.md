# Word frequency lists based on AI generated children's stories

This repository contains **word frequency lists** based on AI generated children's stories, and the code to generate them.

## How to use

- Create a .env file based on the .env.example file.
- (Optional) Run `generate_titles.py` to generate titles for the stories.
- Run `generate_stories.py` to generate the stories.
- (Optional) Download [stories.zip](https://github.com/Rct567/wf_lists_lm_childrenstories/releases) to get the generated stories currently used.
- Run `generate_wf_lists.py` to generate the word frequencies lists.

# Word frequency lists overview

| Language | Word count | Story count |
| --- | --- | --- |
| [English](wf_lists/wf_list_en.csv) | 25,047 | 4,621 |
| [Chinese](wf_lists/wf_list_zh.csv) | 32,361 | 4,334 |
| [French](wf_lists/wf_list_fr.csv) | 34,370 | 4,333 |
| [Spanish](wf_lists/wf_list_es.csv) | 31,351 | 4,332 |
| [Russian](wf_lists/wf_list_ru.csv) | 58,164 | 4,302 |
| [Japanese](wf_lists/wf_list_ja.csv) | 18,789 | 4,298 |
| [Arabic](wf_lists/wf_list_ar.csv) | 81,599 | 4,190 |
| [Italian](wf_lists/wf_list_it.csv) | 32,807 | 3,889 |
| [Portuguese (Portugal)](wf_lists/wf_list_pt.csv) | 31,269 | 3,887 |
| [German](wf_lists/wf_list_de.csv) | 33,890 | 3,885 |
| [Dutch](wf_lists/wf_list_nl.csv) | 25,312 | 3,546 |
| [Portuguese (Brazil)](wf_lists/wf_list_pt_br.csv) | 25,158 | 2,855 |
| [Greek (Modern)](wf_lists/wf_list_el.csv) | 28,490 | 2,851 |
| [Persian](wf_lists/wf_list_fa.csv) | 17,352 | 2,851 |
| [Indonesian](wf_lists/wf_list_id.csv) | 14,090 | 2,849 |
| [Polish](wf_lists/wf_list_pl.csv) | 48,714 | 2,848 |
| [Danish](wf_lists/wf_list_da.csv) | 23,032 | 2,845 |
| [Swedish](wf_lists/wf_list_sv.csv) | 23,660 | 2,844 |
| [Vietnamese](wf_lists/wf_list_vi.csv) | 4,718 | 2,837 |
| [Hungarian](wf_lists/wf_list_hu.csv) | 54,809 | 2,834 |
| [Thai](wf_lists/wf_list_th.csv) | 12,133 | 2,815 |
| [Korean](wf_lists/wf_list_ko.csv) | 53,976 | 2,812 |
| [Turkish](wf_lists/wf_list_tr.csv) | 48,930 | 2,806 |
| [Finnish](wf_lists/wf_list_fi.csv) | 49,192 | 2,802 |
| [Norwegian Bokmål](wf_lists/wf_list_nb.csv) | 21,953 | 2,685 |
| [Hebrew](wf_lists/wf_list_he.csv) | 36,809 | 2,673 |
| [Icelandic](wf_lists/wf_list_is.csv) | 33,607 | 2,663 |
| [Catalan](wf_lists/wf_list_ca.csv) | 27,091 | 2,657 |
| [Latvian](wf_lists/wf_list_lv.csv) | 41,461 | 2,645 |
| [Galician](wf_lists/wf_list_gl.csv) | 30,123 | 2,509 |
| [Macedonian](wf_lists/wf_list_mk.csv) | 31,607 | 2,504 |
| [Bulgarian](wf_lists/wf_list_bg.csv) | 35,360 | 2,498 |
| [Albanian](wf_lists/wf_list_sq.csv) | 25,120 | 2,497 |
| [Ukrainian](wf_lists/wf_list_uk.csv) | 45,215 | 2,497 |
| [Tagalog](wf_lists/wf_list_tl.csv) | 17,361 | 2,493 |
| [Bosnian](wf_lists/wf_list_bs.csv) | 40,140 | 2,490 |
| [Croatian](wf_lists/wf_list_hr.csv) | 40,484 | 2,487 |
| [Slovak](wf_lists/wf_list_sk.csv) | 45,888 | 2,485 |
| [Urdu](wf_lists/wf_list_ur.csv) | 11,600 | 2,485 |
| [Czech](wf_lists/wf_list_cs.csv) | 46,853 | 2,481 |
| [Romanian](wf_lists/wf_list_ro.csv) | 28,002 | 2,480 |
| [Slovenian](wf_lists/wf_list_sl.csv) | 40,347 | 2,474 |
| [Estonian](wf_lists/wf_list_et.csv) | 40,819 | 2,473 |
| [Serbian](wf_lists/wf_list_sr.csv) | 55,198 | 2,473 |
| [Lithuanian](wf_lists/wf_list_lt.csv) | 43,139 | 2,463 |
| [Georgian](wf_lists/wf_list_ka.csv) | 37,157 | 2,451 |
| [Basque](wf_lists/wf_list_eu.csv) | 27,357 | 2,449 |
| [Malay](wf_lists/wf_list_ms.csv) | 13,471 | 2,421 |
| [Esperanto](wf_lists/wf_list_eo.csv) | 26,176 | 2,419 |
| [Armenian](wf_lists/wf_list_hy.csv) | 23,767 | 1,909 |
| [Hindi](wf_lists/wf_list_hi.csv) | 1,663 | 1,745 |
| [Afrikaans](wf_lists/wf_list_af.csv) | 14,785 | 1,739 |
| [Malayalam](wf_lists/wf_list_ml.csv) | 3,253 | 1,738 |
| [Breton](wf_lists/wf_list_br.csv) | 18,900 | 1,698 |
| [Sinhala](wf_lists/wf_list_si.csv) | 3,384 | 1,663 |
| [Kazakh](wf_lists/wf_list_kk.csv) | 27,560 | 1,648 |
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