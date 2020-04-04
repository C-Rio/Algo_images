import numpy

def seuil_otsu(im):
    var_min = numpy.var(im)*len(im[im>=0])
    best_seuil=0

    for s in range(1, 255):
        #Groupe 1 : pixels <s
        card_G1 = len(im[im<s])
        card_G2 = len(im[im>=s])



        if(card_G1 >0 and card_G2>0):
            var_G1 = numpy.var(im[im<s])
            var_G2 = numpy.var(im[im>=s])



            var_intra = card_G1*var_G1 + card_G2*var_G2

            if(var_intra < var_min):
                var_min = var_intra
                best_seuil = s

    return best_seuil