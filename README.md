# Word frequency lists bases on AI generated children's stories

This repository contains **word frequency lists** based on AI generated children's stories, and the code to generate them.

## How to use

- Create a .env file based on the .env.example file.
- (Optional) Run `generate_titles.py` to generate titles for the stories.
- Run `generate_stories.py` to generate the stories.
- Run `generate_wf_lists.py` to generate the word frequencies lists.

## Word frequency lists overview

| Language | Word count | Story count |
| --- | --- | --- |
| [English](wf_lists\wf_list_en.csv) | 19,409 | 2,586 |
| [Spanish](wf_lists\wf_list_es.csv) | 22,684 | 2,586 |
| [Russian](wf_lists\wf_list_ru.csv) | 41,329 | 2,585 |
| [Chinese](wf_lists\wf_list_zh.csv) | 22,521 | 2,585 |
| [Japanese](wf_lists\wf_list_ja.csv) | 11,687 | 2,582 |
| [Dutch](wf_lists\wf_list_nl.csv) | 19,469 | 2,550 |
| [Arabic](wf_lists\wf_list_ar.csv) | 50,627 | 2,421 |
| [German](wf_lists\wf_list_de.csv) | 21,747 | 2,105 |
| [French](wf_lists\wf_list_fr.csv) | 22,481 | 2,100 |
| [Italian](wf_lists\wf_list_it.csv) | 22,516 | 2,098 |
| [Portuguese (Portugal)](wf_lists\wf_list_pt.csv) | 21,381 | 2,097 |
| [Persian](wf_lists\wf_list_fa.csv) | 12,333 | 1,690 |
| [Hungarian](wf_lists\wf_list_hu.csv) | 33,496 | 1,690 |
| [Indonesian](wf_lists\wf_list_id.csv) | 10,158 | 1,687 |
| [Danish](wf_lists\wf_list_da.csv) | 15,262 | 1,686 |
| [Vietnamese](wf_lists\wf_list_vi.csv) | 4,035 | 1,686 |
| [Portuguese (Brazil)](wf_lists\wf_list_pt_br.csv) | 17,865 | 1,685 |
| [Swedish](wf_lists\wf_list_sv.csv) | 15,866 | 1,685 |
| [Thai](wf_lists\wf_list_th.csv) | 8,780 | 1,684 |
| [Greek (Modern)](wf_lists\wf_list_el.csv) | 19,292 | 1,683 |
| [Polish](wf_lists\wf_list_pl.csv) | 31,779 | 1,682 |
| [Turkish](wf_lists\wf_list_tr.csv) | 30,702 | 1,678 |
| [Korean](wf_lists\wf_list_ko.csv) | 32,558 | 1,675 |
| [Finnish](wf_lists\wf_list_fi.csv) | 30,669 | 1,668 |
| [Norwegian Nynorsk](wf_lists\wf_list_nn.csv) | 12,532 | 1,112 |
| [Norwegian](wf_lists\wf_list_no.csv) | 11,517 | 1,112 |
| [Welsh](wf_lists\wf_list_cy.csv) | 11,467 | 1,111 |
| [Hebrew](wf_lists\wf_list_he.csv) | 19,155 | 1,111 |
| [Armenian](wf_lists\wf_list_hy.csv) | 13,887 | 1,110 |
| [Icelandic](wf_lists\wf_list_is.csv) | 16,133 | 1,110 |
| [Catalan](wf_lists\wf_list_ca.csv) | 14,217 | 1,109 |
| [Hindi](wf_lists\wf_list_hi.csv) | 1,404 | 1,109 |
| [Latvian](wf_lists\wf_list_lv.csv) | 19,928 | 1,109 |
| [Khmer](wf_lists\wf_list_km.csv) | 4,948 | 1,107 |
| [Macedonian](wf_lists\wf_list_mk.csv) | 15,771 | 947 |
| [Bulgarian](wf_lists\wf_list_bg.csv) | 17,434 | 944 |
| [Bosnian](wf_lists\wf_list_bs.csv) | 19,039 | 944 |
| [Galician](wf_lists\wf_list_gl.csv) | 14,656 | 944 |
| [Afrikaans](wf_lists\wf_list_af.csv) | 9,238 | 943 |
| [Lithuanian](wf_lists\wf_list_lt.csv) | 18,488 | 941 |
| [Malayalam](wf_lists\wf_list_ml.csv) | 2,161 | 941 |
| [Tagalog](wf_lists\wf_list_tl.csv) | 8,432 | 941 |
| [Esperanto](wf_lists\wf_list_eo.csv) | 12,592 | 939 |
| [Punjabi](wf_lists\wf_list_pa.csv) | 1,380 | 939 |
| [Romanian](wf_lists\wf_list_ro.csv) | 14,252 | 939 |
| [Estonian](wf_lists\wf_list_et.csv) | 17,788 | 938 |
| [Western Frisian](wf_lists\wf_list_fy.csv) | 11,177 | 938 |
| [Croatian](wf_lists\wf_list_hr.csv) | 18,727 | 938 |
| [Romansh](wf_lists\wf_list_rm.csv) | 18,949 | 938 |
| [Slovak](wf_lists\wf_list_sk.csv) | 20,415 | 936 |
| [Slovenian](wf_lists\wf_list_sl.csv) | 18,437 | 934 |
| [Ukrainian](wf_lists\wf_list_uk.csv) | 20,455 | 934 |
| [Urdu](wf_lists\wf_list_ur.csv) | 6,658 | 934 |
| [Belarusian](wf_lists\wf_list_be.csv) | 20,332 | 933 |
| [Albanian](wf_lists\wf_list_sq.csv) | 12,115 | 933 |
| [Czech](wf_lists\wf_list_cs.csv) | 20,720 | 932 |
| [Bengali (Bangla script)](wf_lists\wf_list_bn.csv) | 1,635 | 929 |
| [Serbian](wf_lists\wf_list_sr.csv) | 23,447 | 928 |
| [Uighur](wf_lists\wf_list_ug.csv) | 15,966 | 926 |
| [Yiddish (Hebrew script)](wf_lists\wf_list_yi.csv) | 9,951 | 925 |
| [Amharic](wf_lists\wf_list_am.csv) | 16,476 | 924 |
| [Georgian](wf_lists\wf_list_ka.csv) | 13,792 | 923 |
| [Nepali](wf_lists\wf_list_ne.csv) | 1,911 | 921 |
| [Tibetan](wf_lists\wf_list_bo.csv) | 7,220 | 917 |
| [Basque](wf_lists\wf_list_eu.csv) | 12,531 | 917 |
| [Sundanese](wf_lists\wf_list_su.csv) | 9,497 | 916 |
| [Haitian](wf_lists\wf_list_ht.csv) | 3,798 | 914 |
| [Latin](wf_lists\wf_list_la.csv) | 15,884 | 910 |
| [Mongolian](wf_lists\wf_list_mn.csv) | 13,652 | 901 |
| [Lao](wf_lists\wf_list_lo.csv) | 6,314 | 894 |
| [Uzbek](wf_lists\wf_list_uz.csv) | 16,377 | 881 |
| [Somali](wf_lists\wf_list_so.csv) | 14,161 | 871 |
| [Scottish Gaelic](wf_lists\wf_list_gd.csv) | 7,121 | 868 |
| [Irish](wf_lists\wf_list_ga.csv) | 8,622 | 867 |
| [Zulu](wf_lists\wf_list_zu.csv) | 24,490 | 853 |
| [Kongo](wf_lists\wf_list_kg.csv) | 10,161 | 823 |
| [Old Church Slavonic](wf_lists\wf_list_cu.csv) | 21,042 | 814 |
| [Telugu](wf_lists\wf_list_te.csv) | 1,587 | 809 |
| [Tamil](wf_lists\wf_list_ta.csv) | 1,124 | 808 |
| [Tajik](wf_lists\wf_list_tg.csv) | 11,753 | 801 |
| [Tatar](wf_lists\wf_list_tt.csv) | 12,592 | 800 |
| [Javanese](wf_lists\wf_list_jv.csv) | 8,576 | 799 |
| [Swahili](wf_lists\wf_list_sw.csv) | 9,874 | 796 |
| [Chechen](wf_lists\wf_list_ce.csv) | 10,991 | 793 |
| [Malagasy](wf_lists\wf_list_mg.csv) | 7,514 | 723 |