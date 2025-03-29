from lib.text_processing import TextProcessing

lowercase_string = TextProcessing.lowercase_string


def test_lowercase_string_chechen():

    word_acceptor = TextProcessing.get_word_accepter("ce")

    test_string_chechen = 'ХIорда'
    # python lower() would incorrectly produce 'хiорда' instead of 'хӏорда'
    assert not word_acceptor(test_string_chechen.lower())
    assert word_acceptor(lowercase_string(test_string_chechen, 'ce'))

    test_sentence = "ХIордан тIехула Ваха Вола, зIакаршца тIеэцначух."
    expected_output = "хӏордан тӏехула ваха вола, зӏакаршца тӏеэцначух."
    assert lowercase_string(test_sentence, 'ce') == expected_output


def test_lowercase_string_turkish():

    test_sentence = "İSTANBUL'DA IŞIKLI BİR GECE – İYİ GECELER!"
    expected_output = "istanbul'da ışıklı bir gece – iyi geceler!"
    assert lowercase_string(test_sentence, 'tr') == expected_output

    word_acceptor = TextProcessing.get_word_accepter("tr")

    tokens = [token for token in TextProcessing.default_tokenizer(test_sentence) if token]
    all_tokens_accepted_with_custom_fn = all(word_acceptor(lowercase_string(token, 'tr')) for token in tokens)
    assert all_tokens_accepted_with_custom_fn
    at_least_one_token_reject_by_native_lower_fn = any(not word_acceptor(token.lower()) for token in tokens)
    assert at_least_one_token_reject_by_native_lower_fn

def test_get_word_tokens_pt_br():

    text = "O Mistério do Tesouro Perdido na Ilha dos Pássaros Falantes e Coloridos. хӏорда"
    tokens = TextProcessing.get_word_tokens_from_text(text, "pt_br", filter_words=True)
    assert tokens ==  ['o', 'mistério', 'do', 'tesouro', 'perdido', 'na', 'ilha', 'dos', 'pássaros', 'falantes', 'e', 'coloridos']

def test_get_word_tokens_lo():

    text = "ຢ່າລືມຕັ້ງໃຈຮຽນເດີ້. Oke?"
    tokens = TextProcessing.get_word_tokens_from_text(text, "lo", filter_words=True)
    assert tokens == ['ຢ່າ', 'ລືມ', 'ຕັ້ງໃຈ', 'ຮຽນ', 'ເດີ້']

def test_has_repeating_token_in_sequence():

    token_sequence = "b a a a".split()
    assert TextProcessing.has_repeating_token_in_sequence(token_sequence)
    assert not TextProcessing.has_repeating_token_in_sequence(token_sequence[0:2])
    assert not TextProcessing.has_repeating_token_in_sequence(token_sequence, min_repeats=4)

def test_has_repeating_multiple_tokens_in_sequence():

    token_sequence = "c a b a b a b a b".split()
    assert TextProcessing.has_repeating_token_in_sequence(token_sequence)

    token_sequence = "a b c a b c a b c a b c".split()
    assert TextProcessing.has_repeating_token_in_sequence(token_sequence, max_pattern_length=4)
    assert TextProcessing.has_repeating_token_in_sequence(token_sequence, max_pattern_length=3)
    assert not TextProcessing.has_repeating_token_in_sequence(token_sequence, max_pattern_length=2)
    assert not TextProcessing.has_repeating_token_in_sequence(token_sequence, max_pattern_length=1)
    assert not TextProcessing.has_repeating_token_in_sequence(token_sequence, min_repeats=5)


