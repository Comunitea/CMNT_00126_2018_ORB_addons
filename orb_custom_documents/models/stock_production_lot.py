# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
import math

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    label_barcode = fields.Char(string='Label Barcode', compute='_get_barcode')
    label_barcode_font = fields.Char(string='Label Barcode Font', compute='_get_barcode')
    label_barcode_text = fields.Char(string='Label Barcode', compute='_get_barcode')
    label_ean13 = fields.Char(string='Label EAN13', compute='_get_barcode')

    # Label Palet
    label_box_ean14 = fields.Char(string='Label Box EAN14', compute='_get_barcode')
    label_palet_ean14 = fields.Char(string='Label Pack EAN14', compute='_get_barcode')

    @api.model
    def get_control_digit(self, ean13):
        """
        Obtiene el código de control a partir de los 12 dígitos del ean13
        """
        res = '1'
        idx = 1
        sum_digits = 0
        for digit in ean13:
            num = int(digit)
            if idx % 2 == 0:  # par position
                num = num * 3
            sum_digits += num
            idx += 1

        nearest_10_mult = math.ceil(sum_digits / 10.0) * 10
        res = nearest_10_mult - sum_digits
        return str(res)
    
    @api.model
    def get_control_digit_palet(self, number):
        """Calculate the EAN check digit for 13-digit numbers. The number passed
           should not have the check bit included."""
        return str((10 - sum((3, 1)[i % 2] * int(n) 
            for i, n in enumerate(reversed(number)))) % 10)

    def _get_barcode(self):
        """
        El barcode debe ser el EAN14, el ean13 lo calculamos a partir de este y
        el código de barras lo compongo con la info del ean13
        """
        for lot in self:
            label_text = ''
            ean13 = ''
            ean13_control = ''
            if lot.product_id.barcode and  lot.product_id.barcode.isdigit():
                if len(lot.product_id.barcode) == 13:
                    ean13 = lot.product_id.barcode
                    palet_ean14 = ean13 + self.get_control_digit_palet(ean13)

                    lot.label_ean13 = ean13
                    lot.label_palet_ean14 = palet_ean14

                    ean12 = lot.label_ean13[:-1]
                    digit = '1'
                    new_ean13 = digit + ean12
                    csum_box = self.get_control_digit_palet(new_ean13)
                    ean14 = new_ean13 + csum_box
                    lot.label_box_ean14 = ean14
            
                    # import pdb; pdb.set_trace()
                    code_type = '(01)'
                    ean12 = ean14[:-1]  # EAN13 sin dígito control (12 sígitos)
                    ean14_1 = ean12[:7]
                    ean14_2 = ean12[7:]
                    batch_type = '(10)'
                    label_text = ' '.join([code_type, ean14_1, ean14_2, csum_box, batch_type, lot.name])
                
                code128 = label_text.replace(' ', '').replace('(', '').replace(')', '')
                lot.label_barcode = code128
                lot.label_barcode_text = label_text

                # Manera no codificada A de calcularlo, cogiendo solo el dñigito de
                # control y añadiendolo al final, poner los char de init y fin
                # Así parece que no lo lee bien
                csum = self.get128digit(lot.label_barcode)
                lot.label_barcode_font = 'Ì' + code128 + chr(csum) + 'Î'
                # lot.label_barcode_font = "Ì01184365539813711002712GÎ"

                # Manera codificada B de calcularlo, pero la funcion encode128 no
                # devuelve bien los caracteres de inicio y final así que los susyituyo
                encode_128_base = self.encode128(lot.label_barcode)
                encode_128 = 'Ì' + encode_128_base [1:-1] + 'Î'
                lot.label_barcode_font = encode_128
        
           

    # Es solo la parte que calcula el chechsum del code128
    def get128digit(self, s):
        ''' Code 128 conversion for a font as described at
            https://en.wikipedia.org/wiki/Code_128 and downloaded
            from http://www.barcodelink.net/barcode-font.php
            Only encodes ASCII characters, does not take advantage of
            FNC4 for bytes with the upper bit set.
            It does not attempt to optimize the length of the string,
            Code B is the default to prefer lower case over control characters.
            Coded for https://stackoverflow.com/q/52710760/5987
        '''
        s = s.encode('ascii').decode('ascii')
        if s.isdigit() and len(s) % 2 == 0:
            # use Code 128C, pairs of digits
            codes = [105]
            for i in range(0, len(s), 2):
                codes.append(int(s[i:i+2], 10))
        else:
            # use Code 128B and shift for Code 128A
            mapping = dict((chr(c), [98, c + 64] if c < 32 else [c - 32]) for c in range(128))
            codes = [104]
            for c in s:
                codes.extend(mapping[c])
        check_digit = (codes[0] + sum(i * x for i,x in enumerate(codes))) % 103
        return check_digit

    # Me devuelve un string donde solo están mal los caracteres de inicio y de fin
    # de mi fuente
    def encode128(self, s):
        ''' Code 128 conversion for a font as described at
            https://en.wikipedia.org/wiki/Code_128 and downloaded
            from http://www.barcodelink.net/barcode-font.php
            Only encodes ASCII characters, does not take advantage of
            FNC4 for bytes with the upper bit set.
            It does not attempt to optimize the length of the string,
            Code B is the default to prefer lower case over control characters.
            Coded for https://stackoverflow.com/q/52710760/5987
        '''
        s = s.encode('ascii').decode('ascii')
        if s.isdigit() and len(s) % 2 == 0:
            # use Code 128C, pairs of digits
            codes = [105]
            for i in range(0, len(s), 2):
                codes.append(int(s[i:i+2], 10))
        else:
            # use Code 128B and shift for Code 128A
            mapping = dict((chr(c), [98, c + 64] if c < 32 else [c - 32]) for c in range(128))
            codes = [104]
            for c in s:
                codes.extend(mapping[c])
        check_digit = (codes[0] + sum(i * x for i,x in enumerate(codes))) % 103
        # return check_digit
        codes.append(check_digit)
        codes.append(106) # stop code
        chars = (b'\xd4' + bytes(range(33,126+1)) + bytes(range(200,211+1))).decode('latin-1')
        return ''.join(chars[x] for x in codes)

