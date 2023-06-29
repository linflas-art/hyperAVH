import unittest
from avhparser import find_numbers

class TestAvhParserFr(unittest.TestCase):
    def assertParse(self, txt, result):
        self.assertEqual(find_numbers(txt, locale='fr'), list(map(str, result)))

    def test_default(self):
        self.assertParse("Rendez-vous au 82 si A, et au 45 sinon.", [82, 45])

    def test_no_number(self):
        self.assertParse("Vous trouvez un anneau de cuivre.", [])

    def test_irrelevant_number(self):
        self.assertParse("Vous faites face à 13 gobelins.", [])

    def test_shortened(self):
        self.assertParse("Préférez-vous vous enfuir (au 18) ou combattre (au 231) ?", [18, 231])

class TestAvhParserEn(unittest.TestCase):
    def assertParse(self, txt, result):
        self.assertEqual(find_numbers(txt, locale='en'), list(map(str, result)))

    def test_default(self):
        self.assertParse("If A, turn to 82. Else, turn to 45.", [82, 45])

    def test_no_number(self):
        self.assertParse("You find a lot of nothing.", [])

    def test_irrelevant_number(self):
        self.assertParse("That orc ate 66 pies! Note it, it might be relevant later.", [])

class TestAvhParserZh(unittest.TestCase):
    def test_not_supported(self):
        with self.assertRaises(ValueError) as cm:
            find_numbers("Imagine it's actually Chinese there.", locale='zh')
        self.assertEqual(str(cm.exception), 'Unsupported locale: "zh"')

class TestAvhParserCustom(unittest.TestCase):
    def assertParse(self, txt, prefix, result):
        self.assertEqual(find_numbers(txt, prefix=prefix), list(map(str, result)))

    def test_some_arrow(self):
        self.assertParse("– J’ai failli mourir un paquet de fois, ça compte ? Par le feu (→ 18), par le ridicule (→ 22)…", "→ ", [18, 22])

    def test_simple_regex_prefix(self):
        self.assertParse("– Si tu insistes, on peut arrêter là (→ 16). Mais tu te prives peut-être d’éléments cruciaux que tu aurais découvert en continuant encore un peu (→ ⧗, 3).", "→( ⧗,)? ", [16, 3])

