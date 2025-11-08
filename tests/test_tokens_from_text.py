from lib.text_processing import TextProcessing


def test_get_word_tokens_pt_br():

    text = "O Mistério do Tesouro Perdido na Ilha dos Pássaros Falantes e Coloridos. хӏорда"
    tokens = TextProcessing.get_word_tokens_from_text(text, "pt_br", filter_words=True)
    assert tokens == ['o', 'mistério', 'do', 'tesouro', 'perdido', 'na', 'ilha', 'dos', 'pássaros', 'falantes', 'e', 'coloridos']


def test_get_word_tokens_lo_filtered():

    text = "ຢ່າລືມຕັ້ງໃຈຮຽນເດີ້. Oke?"
    tokens = TextProcessing.get_word_tokens_from_text(text, "lo", filter_words=True)
    assert tokens == ['ຢ່າ', 'ລືມ', 'ຕັ້ງໃຈ', 'ຮຽນ', 'ເດີ້']


def test_get_word_tokens_zh():

    text = "我爱自然语言处理。"
    tokens = TextProcessing.get_word_tokens_from_text(text, "zh", filter_words=True)
    assert tokens == ['我', '爱', '自然语言', '处理']


def test_get_word_tokens_ja():

    text = "私の名前は太郎です 。"
    tokens = TextProcessing.get_word_tokens_from_text(text, "ja", filter_words=True)
    assert tokens == ["私", "の", "名前", "は", "太郎", "です"]


def test_get_word_tokens_th() -> None:

    text: str = "ฉันรักการประมวลผลภาษาธรรมชาติ"
    tokens = TextProcessing.get_word_tokens_from_text(text, "th", filter_words=True)
    assert tokens == ['ฉัน', 'รัก', 'การประมวลผล', 'ภาษาธรรมชาติ']


def test_get_word_tokens_lo() -> None:

    text: str = "ຂ້ອຍຮັກການປະມວນຜົນພາສາທຳມະຊາດ"
    tokens = TextProcessing.get_word_tokens_from_text(text, "lo", filter_words=True)
    assert tokens == ['ຂ້ອຍ', 'ຮັກ', 'ການປະມວນ', 'ຜົນ', 'ພາສາ', 'ທຳມະຊາດ']


def test_get_word_tokens_km() -> None:

    text: str = "ខ្ញុំស្រលាញ់ការដំណើរការភាសាធម្មជាតិ"
    tokens = TextProcessing.get_word_tokens_from_text(text, "km", filter_words=True)
    assert tokens == ['ខ្ញុំ', 'ស្រលាញ់', 'ការដំណើរការ', 'ភាសា', 'ធម្មជាតិ']


# def test_get_word_tokens_my() -> None:

#     text: str = "ကျွန်တော် သဘာဝ ဘာသာစကား စီမံဆောင်ရွက်ခြင်းကို ချစ်တယ်။"
#     tokens = TextProcessing.get_word_tokens_from_text(text, "my", filter_words=True)
#     assert tokens == ['ကျွန်တော်', 'သဘာဝ', 'ဘာသာစကား', 'စီမံဆောင်ရွက်ခြင်း', 'ကို', 'ချစ်', 'တယ်']


def test_get_word_tokens_bo() -> None:
    """Test Tibetan word tokenization."""
    text: str = "ང་རང་བྱུང་སྐད་ཡིག་སྒྲིག་འཇུག་ལ་དགའ།"
    tokens = TextProcessing.get_word_tokens_from_text(text, "bo", filter_words=True)
    assert tokens == ['ང་རང་', 'བྱུང་', 'སྐད་ཡིག་', 'སྒྲིག་', 'འཇུག་', 'ལ་', 'དགའ']
