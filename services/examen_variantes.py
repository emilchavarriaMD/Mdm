"""Redacciones alternativas (misma positividad) de cada hallazgo del examen físico."""
VARIANTES = {'adenopatías cervicales anteriores dolorosas': ['adenopatías cervicales anteriores dolorosas',
                                                 'adenopatías dolorosas en la cadena cervical anterior',
                                                 'se palpan adenopatías cervicales anteriores dolorosas',
                                                 'ganglios cervicales anteriores aumentados de tamaño y dolorosos',
                                                 'cadena cervical anterior con adenopatías dolorosas a la palpación'],
 'adenopatías cervicales duras y fijas': ['adenopatías cervicales duras y fijas',
                                          'adenopatías cervicales de consistencia dura y fijas',
                                          'adenopatías cervicales fijas y duras',
                                          'presencia de adenopatías cervicales duras, fijas a planos',
                                          'ganglios cervicales aumentados de tamaño, duros y fijos'],
 'adenopatías cervicales múltiples, móviles, de consistencia elástica': ['adenopatías cervicales múltiples, móviles, de consistencia elástica',
                                                                         'múltiples adenopatías cervicales móviles, de consistencia elástica',
                                                                         'adenopatías cervicales múltiples de consistencia elástica y móviles',
                                                                         'ganglios cervicales aumentados de tamaño, múltiples, móviles y de consistencia elástica',
                                                                         'linfadenopatías cervicales múltiples, móviles y elásticas'],
 'agudeza visual disminuida, pupilas isocóricas normorreactivas, conjuntivas rosadas': ['agudeza visual disminuida, pupilas isocóricas normorreactivas, conjuntivas rosadas',
                                                                                        'disminución de la agudeza visual, con pupilas isocóricas normorreactivas y conjuntivas rosadas',
                                                                                        'pupilas isocóricas normorreactivas y conjuntivas rosadas, con agudeza visual disminuida',
                                                                                        'conjuntivas rosadas, pupilas isocóricas normorreactivas y agudeza visual disminuida',
                                                                                        'agudeza visual reducida; pupilas isocóricas, normorreactivas; conjuntivas rosadas'],
 'agudeza visual disminuida; fondo de ojo con alteraciones retinianas': ['agudeza visual disminuida; fondo de ojo con alteraciones retinianas',
                                                                         'disminución de la agudeza visual; alteraciones retinianas en el fondo de ojo',
                                                                         'agudeza visual disminuida, con alteraciones retinianas al examen de fondo de ojo',
                                                                         'fondo de ojo con alteraciones retinianas; agudeza visual disminuida',
                                                                         'con disminución de la agudeza visual y alteraciones retinianas en la fundoscopia'],
 'altura uterina acorde o discordante con la edad gestacional, frecuencia cardíaca fetal presente': ['altura uterina acorde o discordante con la edad gestacional, frecuencia cardíaca fetal presente',
                                                                                                     'altura uterina acorde o discordante con la edad gestacional, con frecuencia cardíaca fetal '
                                                                                                     'presente',
                                                                                                     'frecuencia cardíaca fetal presente, altura uterina acorde o discordante con la edad gestacional',
                                                                                                     'altura uterina acorde o discordante con la edad gestacional; latido cardíaco fetal presente',
                                                                                                     'con frecuencia cardíaca fetal presente y altura uterina acorde o discordante con la edad '
                                                                                                     'gestacional'],
 'altura uterina acorde; frecuencia cardíaca fetal presente': ['altura uterina acorde; frecuencia cardíaca fetal presente',
                                                               'altura uterina acorde, con frecuencia cardíaca fetal presente',
                                                               'frecuencia cardíaca fetal presente; altura uterina acorde',
                                                               'altura uterina acorde a lo esperado; latido cardíaco fetal presente',
                                                               'con frecuencia cardíaca fetal presente y altura uterina acorde'],
 'asimetría facial con desviación de la comisura labial, borramiento del surco nasolabial e imposibilidad para cerrar el ojo del lado afectado': ['asimetría facial con desviación de la comisura '
                                                                                                                                                  'labial, borramiento del surco nasolabial e '
                                                                                                                                                  'imposibilidad para cerrar el ojo del lado afectado',
                                                                                                                                                  'asimetría facial, con desviación de la comisura '
                                                                                                                                                  'labial, borramiento del surco nasolabial e '
                                                                                                                                                  'incapacidad para cerrar el ojo del lado afectado',
                                                                                                                                                  'desviación de la comisura labial y borramiento del '
                                                                                                                                                  'surco nasolabial con asimetría facial, e '
                                                                                                                                                  'imposibilidad para cerrar el ojo del lado afectado',
                                                                                                                                                  'imposibilidad de cerrar el ojo del lado afectado, '
                                                                                                                                                  'con asimetría facial, desviación de la comisura '
                                                                                                                                                  'labial y borramiento del surco nasolabial',
                                                                                                                                                  'cara asimétrica con borramiento del surco '
                                                                                                                                                  'nasolabial, desviación de la comisura labial e '
                                                                                                                                                  'incapacidad de cerrar el ojo del lado afectado'],
 'aumento de volumen escrotal doloroso, con eritema o masa a la palpación': ['aumento de volumen escrotal doloroso, con eritema o masa a la palpación',
                                                                             'escroto aumentado de volumen y doloroso, con eritema o masa a la palpación',
                                                                             'aumento de volumen doloroso del escroto, con eritema o masa palpable',
                                                                             'dolor y aumento de volumen escrotal, con eritema o masa a la palpación',
                                                                             'escroto doloroso y aumentado de tamaño, con eritema o masa palpable'],
 'borde palpebral eritematoso con escamas y costras': ['borde palpebral eritematoso con escamas y costras',
                                                       'borde palpebral con eritema, escamas y costras',
                                                       'eritema del borde palpebral con escamas y costras',
                                                       'escamas y costras en el borde palpebral eritematoso',
                                                       'márgenes palpebrales eritematosos, con escamas y costras'],
 'borde ungueal del dedo gordo del pie con eritema, edema, dolor y tejido de granulación': ['borde ungueal del dedo gordo del pie con eritema, edema, dolor y tejido de granulación',
                                                                                            'dedo gordo del pie con eritema, edema, dolor y tejido de granulación en el borde ungueal',
                                                                                            'eritema, edema y dolor en el borde ungueal del dedo gordo del pie, con tejido de granulación',
                                                                                            'pliegue ungueal del hallux con eritema, edema, dolor y tejido de granulación',
                                                                                            'borde ungueal del primer dedo del pie eritematoso, edematoso y doloroso, con tejido de granulación'],
 'caries con destrucción coronaria, dolor a la percusión de la pieza, encía eritematosa y edematosa, con o sin fístula o drenaje purulento': ['caries con destrucción coronaria, dolor a la percusión '
                                                                                                                                              'de la pieza, encía eritematosa y edematosa, con o sin '
                                                                                                                                              'fístula o drenaje purulento',
                                                                                                                                              'caries con destrucción coronaria, dolor a la percusión '
                                                                                                                                              'de la pieza dental, encía eritematosa y edematosa, con '
                                                                                                                                              'o sin fístula o drenaje purulento',
                                                                                                                                              'pieza dental con caries y destrucción coronaria, '
                                                                                                                                              'dolorosa a la percusión, con encía eritematosa y '
                                                                                                                                              'edematosa, con o sin fístula o drenaje purulento',
                                                                                                                                              'encía eritematosa y edematosa, caries con destrucción '
                                                                                                                                              'coronaria y dolor a la percusión de la pieza; puede '
                                                                                                                                              'haber fístula o drenaje purulento',
                                                                                                                                              'destrucción coronaria por caries con dolor a la '
                                                                                                                                              'percusión dental, encía hiperémica y edematosa, con o '
                                                                                                                                              'sin fístula o drenaje purulento'],
 'conducto auditivo con eritema leve y membrana timpánica con alteraciones': ['conducto auditivo con eritema leve y membrana timpánica con alteraciones',
                                                                              'conducto auditivo con leve eritema y alteraciones de la membrana timpánica',
                                                                              'membrana timpánica con alteraciones y conducto auditivo con eritema leve',
                                                                              'eritema leve del conducto auditivo y membrana timpánica alterada',
                                                                              'conducto auditivo levemente eritematoso, con membrana timpánica alterada'],
 'conducto auditivo externo eritematoso, edematoso y doloroso a la tracción del pabellón, con secreción': ['conducto auditivo externo eritematoso, edematoso y doloroso a la tracción del pabellón, '
                                                                                                           'con secreción',
                                                                                                           'conducto auditivo externo con eritema, edema y secreción, doloroso a la tracción del '
                                                                                                           'pabellón',
                                                                                                           'conducto auditivo externo eritematoso y edematoso, con secreción y dolor a la tracción del '
                                                                                                           'pabellón',
                                                                                                           'dolor a la tracción del pabellón, con conducto auditivo externo eritematoso, edematoso y '
                                                                                                           'con secreción',
                                                                                                           'conducto auditivo externo con secreción, eritema y edema, doloroso al traccionar el '
                                                                                                           'pabellón'],
 'conducto auditivo externo ocluido por tapón de cerumen, membrana timpánica no visualizable': ['conducto auditivo externo ocluido por tapón de cerumen, membrana timpánica no visualizable',
                                                                                                'conducto auditivo externo obstruido por tapón de cerumen, con membrana timpánica no visualizable',
                                                                                                'tapón de cerumen que ocluye el conducto auditivo externo, impidiendo visualizar la membrana timpánica',
                                                                                                'membrana timpánica no visualizable por tapón de cerumen que ocluye el conducto auditivo externo',
                                                                                                'conducto auditivo externo con tapón de cerumen oclusivo, sin visualización de la membrana timpánica'],
 'conjuntiva hiperémica, con secreción mucopurulenta o serosa y edema palpebral; agudeza visual conservada': ['conjuntiva hiperémica, con secreción mucopurulenta o serosa y edema palpebral; agudeza '
                                                                                                              'visual conservada',
                                                                                                              'conjuntiva hiperémica con secreción serosa o mucopurulenta y edema palpebral; agudeza '
                                                                                                              'visual conservada',
                                                                                                              'hiperemia conjuntival con secreción mucopurulenta o serosa y edema palpebral; agudeza '
                                                                                                              'visual conservada',
                                                                                                              'agudeza visual conservada; conjuntiva hiperémica, con secreción mucopurulenta o serosa '
                                                                                                              'y edema de los párpados',
                                                                                                              'conjuntiva eritematosa, con secreción serosa o mucopurulenta y edema palpebral; sin '
                                                                                                              'alteración de la agudeza visual'],
 'conjuntivas pálidas': ['conjuntivas pálidas', 'palidez conjuntival', 'conjuntivas con palidez', 'conjuntivas de aspecto pálido', 'conjuntivas hipocrómicas, pálidas'],
 'contractura de la musculatura cervical posterior': ['contractura de la musculatura cervical posterior',
                                                      'musculatura cervical posterior contracturada',
                                                      'contractura muscular cervical posterior',
                                                      'contractura de los músculos de la región cervical posterior',
                                                      'región cervical posterior con contractura muscular'],
 'contractura de la musculatura paravertebral cervical y trapecio, dolor a la palpación y limitación para los movimientos de rotación y flexión': ['contractura de la musculatura paravertebral '
                                                                                                                                                   'cervical y trapecio, dolor a la palpación y '
                                                                                                                                                   'limitación para los movimientos de rotación y '
                                                                                                                                                   'flexión',
                                                                                                                                                   'contractura de la musculatura paravertebral '
                                                                                                                                                   'cervical y del trapecio, con dolor a la palpación '
                                                                                                                                                   'y limitación de los movimientos de rotación y '
                                                                                                                                                   'flexión',
                                                                                                                                                   'dolor a la palpación y contractura de la '
                                                                                                                                                   'musculatura paravertebral cervical y trapecio, con '
                                                                                                                                                   'limitación para la rotación y la flexión',
                                                                                                                                                   'limitación para los movimientos de rotación y '
                                                                                                                                                   'flexión, con contractura de la musculatura '
                                                                                                                                                   'paravertebral cervical y trapecio y dolor a la '
                                                                                                                                                   'palpación',
                                                                                                                                                   'musculatura paravertebral cervical y trapecio '
                                                                                                                                                   'contracturados y dolorosos a la palpación, con '
                                                                                                                                                   'limitación de la rotación y flexión'],
 'cuello uterino sin lesiones, con hilos del dispositivo intrauterino visibles en el orificio cervical y sin dolor a la movilización': ['cuello uterino sin lesiones, con hilos del dispositivo '
                                                                                                                                        'intrauterino visibles en el orificio cervical y sin dolor a '
                                                                                                                                        'la movilización',
                                                                                                                                        'cérvix sin lesiones, con hilos del DIU visibles a través del '
                                                                                                                                        'orificio cervical, sin dolor a la movilización cervical',
                                                                                                                                        'orificio cervical con hilos del dispositivo intrauterino '
                                                                                                                                        'visibles, cuello uterino sin lesiones y movilización cervical '
                                                                                                                                        'indolora',
                                                                                                                                        'se observan los hilos del dispositivo intrauterino en el '
                                                                                                                                        'orificio cervical, cuello uterino sin lesiones y sin dolor al '
                                                                                                                                        'movilizarlo',
                                                                                                                                        'cuello uterino de aspecto normal, sin lesiones, con hilos del '
                                                                                                                                        'DIU visibles en el orificio cervical externo y sin dolor a la '
                                                                                                                                        'movilización'],
 'cuerpo extraño visible en conducto auditivo externo con eritema local': ['cuerpo extraño visible en conducto auditivo externo con eritema local',
                                                                           'cuerpo extraño visible en el conducto auditivo externo, con eritema local',
                                                                           'eritema local con cuerpo extraño visible en conducto auditivo externo',
                                                                           'se visualiza cuerpo extraño en conducto auditivo externo, con eritema local',
                                                                           'conducto auditivo externo con cuerpo extraño visible y eritema local'],
 'deformidad, edema, equimosis y dolor intenso a la palpación del foco, con impotencia funcional; pulsos y sensibilidad distal conservados': ['deformidad, edema, equimosis y dolor intenso a la '
                                                                                                                                              'palpación del foco, con impotencia funcional; pulsos y '
                                                                                                                                              'sensibilidad distal conservados',
                                                                                                                                              'deformidad, edema y equimosis, con dolor intenso a la '
                                                                                                                                              'palpación del foco e impotencia funcional; pulsos y '
                                                                                                                                              'sensibilidad distal conservados',
                                                                                                                                              'dolor intenso a la palpación del foco, con deformidad, '
                                                                                                                                              'edema, equimosis e impotencia funcional; sensibilidad y '
                                                                                                                                              'pulsos distales conservados',
                                                                                                                                              'impotencia funcional con deformidad, edema, equimosis y '
                                                                                                                                              'dolor intenso a la palpación del foco, con pulsos y '
                                                                                                                                              'sensibilidad distal conservados',
                                                                                                                                              'edema, equimosis y deformidad con dolor intenso a la '
                                                                                                                                              'palpación del foco e impotencia funcional; sin '
                                                                                                                                              'alteración de pulsos ni de sensibilidad distal'],
 'descamación, maceración y fisuras en espacios interdigitales de los pies, con eritema': ['descamación, maceración y fisuras en espacios interdigitales de los pies, con eritema',
                                                                                           'eritema con descamación, maceración y fisuras en los espacios interdigitales de los pies',
                                                                                           'espacios interdigitales de los pies con eritema, descamación, maceración y fisuras',
                                                                                           'maceración, descamación y fisuras interdigitales en los pies, con eritema',
                                                                                           'pies con fisuras, maceración y descamación en espacios interdigitales, acompañadas de eritema'],
 'desviación del primer dedo del pie con prominencia ósea medial, dolorosa, con eritema y callosidad': ['desviación del primer dedo del pie con prominencia ósea medial, dolorosa, con eritema y '
                                                                                                        'callosidad',
                                                                                                        'desviación del primer dedo del pie con prominencia ósea medial dolorosa, eritema y callosidad',
                                                                                                        'prominencia ósea medial dolorosa, con eritema y callosidad, por desviación del primer dedo '
                                                                                                        'del pie',
                                                                                                        'primer dedo del pie desviado, con prominencia ósea medial dolorosa, eritematosa y con '
                                                                                                        'callosidad',
                                                                                                        'desviación del hallux con prominencia ósea medial, dolor, eritema y callosidad'],
 'disminución de la fuerza proximal, marcha anserina y atrofia muscular': ['disminución de la fuerza proximal, marcha anserina y atrofia muscular',
                                                                           'fuerza proximal disminuida, con marcha anserina y atrofia muscular',
                                                                           'marcha anserina, atrofia muscular y disminución de la fuerza proximal',
                                                                           'atrofia muscular y marcha anserina, con fuerza proximal disminuida',
                                                                           'debilidad muscular proximal con marcha anserina y atrofia muscular'],
 'disminución de la sensibilidad en guante y calcetín, con reflejos osteotendinosos disminuidos': ['disminución de la sensibilidad en guante y calcetín, con reflejos osteotendinosos disminuidos',
                                                                                                   'sensibilidad disminuida en guante y calcetín, con reflejos osteotendinosos disminuidos',
                                                                                                   'reflejos osteotendinosos disminuidos y disminución de la sensibilidad en guante y calcetín',
                                                                                                   'hipoestesia en guante y calcetín, con hiporreflexia osteotendinosa',
                                                                                                   'con reflejos osteotendinosos disminuidos y sensibilidad disminuida en distribución de guante y '
                                                                                                   'calcetín'],
 'disminución del murmullo vesicular con estertores crepitantes localizados y aumento de las vibraciones vocales en el área afectada': ['disminución del murmullo vesicular con estertores crepitantes '
                                                                                                                                        'localizados y aumento de las vibraciones vocales en el área '
                                                                                                                                        'afectada',
                                                                                                                                        'murmullo vesicular disminuido, con estertores crepitantes '
                                                                                                                                        'localizados y vibraciones vocales aumentadas en el área '
                                                                                                                                        'afectada',
                                                                                                                                        'estertores crepitantes localizados con disminución del '
                                                                                                                                        'murmullo vesicular y aumento de las vibraciones vocales en el '
                                                                                                                                        'área afectada',
                                                                                                                                        'en el área afectada, aumento de las vibraciones vocales, '
                                                                                                                                        'disminución del murmullo vesicular y estertores crepitantes '
                                                                                                                                        'localizados',
                                                                                                                                        'murmullo vesicular disminuido y crepitantes localizados, con '
                                                                                                                                        'vibraciones vocales aumentadas en el área afectada'],
 'dolor a la palpación de columna, cifosis dorsal leve y disminución de la talla': ['dolor a la palpación de columna, cifosis dorsal leve y disminución de la talla',
                                                                                    'dolor a la palpación de la columna, con cifosis dorsal leve y disminución de la talla',
                                                                                    'cifosis dorsal leve, dolor a la palpación de columna y disminución de la talla',
                                                                                    'disminución de la talla, con cifosis dorsal leve y dolor a la palpación de la columna',
                                                                                    'columna dolorosa a la palpación, con cifosis dorsal leve y talla disminuida'],
 'dolor a la palpación de la musculatura paravertebral lumbar, con contractura y limitación a la flexión; Lasègue positivo si hay irradiación, fuerza y sensibilidad conservadas': ['dolor a la '
                                                                                                                                                                                    'palpación de la '
                                                                                                                                                                                    'musculatura '
                                                                                                                                                                                    'paravertebral '
                                                                                                                                                                                    'lumbar, con '
                                                                                                                                                                                    'contractura y '
                                                                                                                                                                                    'limitación a la '
                                                                                                                                                                                    'flexión; Lasègue '
                                                                                                                                                                                    'positivo si hay '
                                                                                                                                                                                    'irradiación, '
                                                                                                                                                                                    'fuerza y '
                                                                                                                                                                                    'sensibilidad '
                                                                                                                                                                                    'conservadas',
                                                                                                                                                                                    'musculatura '
                                                                                                                                                                                    'paravertebral '
                                                                                                                                                                                    'lumbar dolorosa a '
                                                                                                                                                                                    'la palpación, con '
                                                                                                                                                                                    'contractura y '
                                                                                                                                                                                    'limitación a la '
                                                                                                                                                                                    'flexión; Lasègue '
                                                                                                                                                                                    'positivo si hay '
                                                                                                                                                                                    'irradiación, '
                                                                                                                                                                                    'fuerza y '
                                                                                                                                                                                    'sensibilidad '
                                                                                                                                                                                    'conservadas',
                                                                                                                                                                                    'contractura y '
                                                                                                                                                                                    'dolor a la '
                                                                                                                                                                                    'palpación de la '
                                                                                                                                                                                    'musculatura '
                                                                                                                                                                                    'paravertebral '
                                                                                                                                                                                    'lumbar, con '
                                                                                                                                                                                    'limitación a la '
                                                                                                                                                                                    'flexión; fuerza y '
                                                                                                                                                                                    'sensibilidad '
                                                                                                                                                                                    'conservadas; '
                                                                                                                                                                                    'Lasègue positivo '
                                                                                                                                                                                    'si hay '
                                                                                                                                                                                    'irradiación',
                                                                                                                                                                                    'dolor y '
                                                                                                                                                                                    'contractura '
                                                                                                                                                                                    'paravertebral '
                                                                                                                                                                                    'lumbar a la '
                                                                                                                                                                                    'palpación, con '
                                                                                                                                                                                    'limitación a la '
                                                                                                                                                                                    'flexión; fuerza y '
                                                                                                                                                                                    'sensibilidad '
                                                                                                                                                                                    'conservadas, '
                                                                                                                                                                                    'Lasègue positivo '
                                                                                                                                                                                    'si hay '
                                                                                                                                                                                    'irradiación',
                                                                                                                                                                                    'limitación a la '
                                                                                                                                                                                    'flexión con dolor '
                                                                                                                                                                                    'a la palpación y '
                                                                                                                                                                                    'contractura de la '
                                                                                                                                                                                    'musculatura '
                                                                                                                                                                                    'paravertebral '
                                                                                                                                                                                    'lumbar; Lasègue '
                                                                                                                                                                                    'positivo si hay '
                                                                                                                                                                                    'irradiación; '
                                                                                                                                                                                    'fuerza y '
                                                                                                                                                                                    'sensibilidad '
                                                                                                                                                                                    'conservadas'],
 'dolor a la palpación en hipogastrio y a la movilización cervical, útero y anexos sin masas': ['dolor a la palpación en hipogastrio y a la movilización cervical, útero y anexos sin masas',
                                                                                                'dolor a la palpación del hipogastrio y a la movilización cervical, útero y anexos sin masas',
                                                                                                'útero y anexos sin masas; dolor a la palpación en hipogastrio y a la movilización cervical',
                                                                                                'hipogastrio doloroso a la palpación y dolor a la movilización cervical, con útero y anexos sin masas',
                                                                                                'dolor hipogástrico a la palpación y a la movilización del cuello uterino, útero y anexos sin masas'],
 'dolor a la palpación y a la movilización articular, crepitación, limitación del rango de movimiento y leve edema articular': ['dolor a la palpación y a la movilización articular, crepitación, '
                                                                                                                                'limitación del rango de movimiento y leve edema articular',
                                                                                                                                'dolor a la palpación y a la movilización de la articulación, con '
                                                                                                                                'crepitación, limitación del rango de movimiento y leve edema '
                                                                                                                                'articular',
                                                                                                                                'crepitación y dolor a la palpación y movilización articular, '
                                                                                                                                'limitación del rango de movimiento y leve edema articular',
                                                                                                                                'leve edema articular, con dolor a la palpación y a la movilización, '
                                                                                                                                'crepitación y limitación del rango de movimiento',
                                                                                                                                'limitación del rango de movimiento, con dolor articular a la '
                                                                                                                                'palpación y movilización, crepitación y leve edema'],
 'dolor a la palpación y a los movimientos de la zona afectada, con limitación funcional leve y sin eritema ni calor marcados': ['dolor a la palpación y a los movimientos de la zona afectada, con '
                                                                                                                                 'limitación funcional leve y sin eritema ni calor marcados',
                                                                                                                                 'zona afectada con dolor a la palpación y a los movimientos, '
                                                                                                                                 'limitación funcional leve y sin eritema ni calor marcados',
                                                                                                                                 'limitación funcional leve, con dolor a la palpación y al movimiento '
                                                                                                                                 'de la zona afectada, sin eritema ni calor marcados',
                                                                                                                                 'dolor a la palpación y al movimiento en la zona afectada, sin '
                                                                                                                                 'eritema ni calor marcados, con leve limitación funcional',
                                                                                                                                 'sin eritema ni calor marcados; dolor a la palpación y a los '
                                                                                                                                 'movimientos de la zona afectada con limitación funcional leve'],
 'dolor a la palpación y contractura muscular en el grupo afectado, con limitación para el estiramiento; sin déficit de fuerza': ['dolor a la palpación y contractura muscular en el grupo afectado, '
                                                                                                                                  'con limitación para el estiramiento; sin déficit de fuerza',
                                                                                                                                  'dolor a la palpación y contractura en el grupo muscular afectado, '
                                                                                                                                  'con limitación para el estiramiento; fuerza conservada',
                                                                                                                                  'contractura y dolor a la palpación del grupo muscular afectado, con '
                                                                                                                                  'limitación para el estiramiento; sin déficit de fuerza',
                                                                                                                                  'grupo muscular afectado con dolor a la palpación y contractura, '
                                                                                                                                  'limitación para el estiramiento y sin déficit de fuerza',
                                                                                                                                  'limitación para el estiramiento, con dolor y contractura muscular a '
                                                                                                                                  'la palpación en el grupo afectado; sin pérdida de fuerza'],
 'dolor desencadenado por la palpación de puntos gatillo en la distribución del trigémino': ['dolor desencadenado por la palpación de puntos gatillo en la distribución del trigémino',
                                                                                             'dolor desencadenado a la palpación de puntos gatillo en la distribución del trigémino',
                                                                                             'puntos gatillo en la distribución del trigémino que desencadenan dolor a la palpación',
                                                                                             'la palpación de puntos gatillo en el territorio del trigémino desencadena dolor',
                                                                                             'dolor provocado al palpar puntos gatillo en el territorio de distribución del nervio trigémino'],
 'dolor suprapúbico a la palpación': ['dolor suprapúbico a la palpación',
                                      'dolor a la palpación suprapúbica',
                                      'región suprapúbica dolorosa a la palpación',
                                      'sensibilidad dolorosa suprapúbica a la palpación',
                                      'dolor a la palpación en el área suprapúbica'],
 'dos orificios punzantes con edema progresivo, equimosis y dolor intenso en el miembro afectado': ['dos orificios punzantes con edema progresivo, equimosis y dolor intenso en el miembro afectado',
                                                                                                    'dos orificios punzantes, con edema progresivo, equimosis y dolor intenso en el miembro afectado',
                                                                                                    'miembro afectado con dos orificios punzantes, edema progresivo, equimosis y dolor intenso',
                                                                                                    'se observan dos orificios punzantes con equimosis, edema progresivo y dolor intenso en el miembro '
                                                                                                    'afectado',
                                                                                                    'edema progresivo, equimosis y dolor intenso en el miembro afectado, con dos orificios punzantes'],
 'edema con fóvea en miembros inferiores, reflejos osteotendinosos aumentados': ['edema con fóvea en miembros inferiores, reflejos osteotendinosos aumentados',
                                                                                 'edema con fóvea en miembros inferiores y reflejos osteotendinosos aumentados',
                                                                                 'reflejos osteotendinosos aumentados, con edema con fóvea en miembros inferiores',
                                                                                 'miembros inferiores con edema con fóvea; reflejos osteotendinosos aumentados',
                                                                                 'edema con signo de fóvea en miembros inferiores, con hiperreflexia osteotendinosa'],
 'edema de miembros inferiores con fóvea': ['edema de miembros inferiores con fóvea',
                                            'edema con fóvea en miembros inferiores',
                                            'miembros inferiores con edema que deja fóvea',
                                            'edema con signo de fóvea en ambos miembros inferiores',
                                            'edema con godet en miembros inferiores'],
 'edema de miembros inferiores con fóvea, várices visibles, hiperpigmentación y cambios tróficos de la piel': ['edema de miembros inferiores con fóvea, várices visibles, hiperpigmentación y cambios '
                                                                                                               'tróficos de la piel',
                                                                                                               'miembros inferiores con edema con fóvea, várices visibles, hiperpigmentación y cambios '
                                                                                                               'tróficos cutáneos',
                                                                                                               'várices visibles y edema con fóvea en miembros inferiores, con hiperpigmentación y '
                                                                                                               'cambios tróficos de la piel',
                                                                                                               'edema con fóvea en miembros inferiores, acompañado de várices visibles, '
                                                                                                               'hiperpigmentación y cambios tróficos de la piel',
                                                                                                               'hiperpigmentación y cambios tróficos de la piel en miembros inferiores, con várices '
                                                                                                               'visibles y edema con fóvea'],
 'edema leve de miembros inferiores': ['edema leve de miembros inferiores',
                                       'edema leve en miembros inferiores',
                                       'miembros inferiores con edema leve',
                                       'leve edema de ambos miembros inferiores',
                                       'discreto edema en miembros inferiores'],
 'edema y equimosis en la articulación afectada, dolor a la palpación y a la movilización, con limitación del apoyo': ['edema y equimosis en la articulación afectada, dolor a la palpación y a la '
                                                                                                                       'movilización, con limitación del apoyo',
                                                                                                                       'articulación afectada con edema y equimosis, dolor a la palpación y a la '
                                                                                                                       'movilización y limitación del apoyo',
                                                                                                                       'dolor a la palpación y a la movilización de la articulación afectada, con '
                                                                                                                       'edema, equimosis y limitación del apoyo',
                                                                                                                       'edema, equimosis y dolor a la palpación y movilización en la articulación '
                                                                                                                       'afectada, con apoyo limitado',
                                                                                                                       'limitación del apoyo, con edema y equimosis en la articulación afectada y '
                                                                                                                       'dolor a la palpación y a la movilización'],
 'edema, calor y dolor en articulaciones pequeñas de manos y muñecas con rigidez, simétricos; limitación para el cierre del puño': ['edema, calor y dolor en articulaciones pequeñas de manos y '
                                                                                                                                    'muñecas con rigidez, simétricos; limitación para el cierre del '
                                                                                                                                    'puño',
                                                                                                                                    'edema, calor y dolor simétricos en articulaciones pequeñas de '
                                                                                                                                    'manos y muñecas, con rigidez; limitación para el cierre del puño',
                                                                                                                                    'articulaciones pequeñas de manos y muñecas con edema, calor, '
                                                                                                                                    'dolor y rigidez, simétricos; limitación para cerrar el puño',
                                                                                                                                    'rigidez, edema, calor y dolor simétricos en pequeñas '
                                                                                                                                    'articulaciones de manos y muñecas; no logra el cierre completo '
                                                                                                                                    'del puño',
                                                                                                                                    'limitación para el cierre del puño; edema, calor y dolor con '
                                                                                                                                    'rigidez en articulaciones pequeñas de manos y muñecas, '
                                                                                                                                    'simétricos'],
 'edema, equimosis y dolor a la palpación en la zona del trauma, con movilidad conservada': ['edema, equimosis y dolor a la palpación en la zona del trauma, con movilidad conservada',
                                                                                             'edema, equimosis y dolor a la palpación en la zona traumatizada, con movilidad conservada',
                                                                                             'zona del trauma con edema, equimosis y dolor a la palpación; movilidad conservada',
                                                                                             'movilidad conservada, con edema, equimosis y dolor a la palpación en el área del trauma',
                                                                                             'dolor a la palpación, edema y equimosis en la región del trauma, sin limitación de la movilidad'],
 'equimosis y hematomas en distintas etapas de evolución, con dolor a la palpación': ['equimosis y hematomas en distintas etapas de evolución, con dolor a la palpación',
                                                                                      'hematomas y equimosis en distintas etapas de evolución, dolorosos a la palpación',
                                                                                      'con dolor a la palpación, equimosis y hematomas en diferentes etapas de evolución',
                                                                                      'equimosis y hematomas de diferentes tiempos de evolución, con dolor a la palpación',
                                                                                      'lesiones equimóticas y hematomas en distintos estadios evolutivos, dolorosos a la palpación'],
 'eritema con erosiones en región del pañal, con pápulas satélite': ['eritema con erosiones en región del pañal, con pápulas satélite',
                                                                     'región del pañal con eritema y erosiones, con pápulas satélite',
                                                                     'eritema y erosiones en área del pañal, acompañados de pápulas satélite',
                                                                     'área del pañal eritematosa y erosionada, con pápulas satélite',
                                                                     'erosiones y eritema en la zona del pañal, con lesiones papulares satélite'],
 'eritema facial y exantema; prueba del torniquete a valorar': ['eritema facial y exantema; prueba del torniquete a valorar',
                                                                'exantema y eritema facial; prueba del torniquete a valorar',
                                                                'eritema en la cara con exantema; se valora prueba del torniquete',
                                                                'prueba del torniquete a valorar, con eritema facial y exantema',
                                                                'rubicundez facial y exantema; pendiente prueba del torniquete'],
 'eritema intenso con ampollas y descamación en áreas expuestas, dolorosas al tacto': ['eritema intenso con ampollas y descamación en áreas expuestas, dolorosas al tacto',
                                                                                       'áreas expuestas con eritema intenso, ampollas y descamación, dolorosas al tacto',
                                                                                       'eritema marcado con ampollas y descamación en zonas expuestas, con dolor al tacto',
                                                                                       'lesiones en áreas expuestas con eritema intenso, flictenas y descamación, dolorosas al contacto',
                                                                                       'descamación, ampollas y eritema intenso en áreas expuestas, dolorosas a la palpación'],
 'escape de orina con la maniobra de Valsalva; cistocele a valorar': ['escape de orina con la maniobra de Valsalva; cistocele a valorar',
                                                                      'pérdida de orina con la maniobra de Valsalva; cistocele a valorar',
                                                                      'con la maniobra de Valsalva, escape de orina; cistocele por valorar',
                                                                      'cistocele a valorar; escape urinario con la maniobra de Valsalva',
                                                                      'escape de orina al realizar la maniobra de Valsalva, con cistocele a valorar'],
 'escleras ictéricas': ['escleras ictéricas', 'escleras con tinte ictérico', 'ictericia escleral', 'escleras de color amarillento (ictéricas)', 'tinte ictérico en escleras'],
 'exantema maculopapular eritematoso': ['exantema maculopapular eritematoso',
                                        'exantema eritematoso de tipo maculopapular',
                                        'erupción maculopapular eritematosa',
                                        'exantema maculopapular de coloración eritematosa',
                                        'lesiones maculopapulares eritematosas en forma de exantema'],
 'excoriaciones y abrasiones superficiales con eritema y costras hemáticas': ['excoriaciones y abrasiones superficiales con eritema y costras hemáticas',
                                                                              'abrasiones y excoriaciones superficiales con eritema y costras hemáticas',
                                                                              'excoriaciones superficiales y abrasiones eritematosas con costras hemáticas',
                                                                              'lesiones superficiales tipo excoriación y abrasión, con eritema y costras hemáticas',
                                                                              'áreas de abrasión y excoriación superficial, eritematosas, cubiertas por costras hemáticas'],
 'faringe hiperémica con amígdalas hipertróficas, eritematosas y con exudado blanquecino': ['faringe hiperémica con amígdalas hipertróficas, eritematosas y con exudado blanquecino',
                                                                                            'faringe eritematosa, con amígdalas hipertróficas, hiperémicas y con exudado blanquecino',
                                                                                            'amígdalas hipertróficas, eritematosas y con exudado blanquecino, con faringe hiperémica',
                                                                                            'faringe con hiperemia y amígdalas aumentadas de tamaño, eritematosas, con exudado blanquecino',
                                                                                            'hiperemia faríngea con hipertrofia amigdalina, eritema y exudado blanquecino'],
 'faringe levemente hiperémica; voz ronca': ['faringe levemente hiperémica; voz ronca',
                                             'faringe con hiperemia leve; voz ronca',
                                             'voz ronca; faringe levemente hiperémica',
                                             'faringe ligeramente eritematosa; voz ronca',
                                             'faringe con leve hiperemia y voz ronca'],
 'faringe muy hiperémica, amígdalas hipertróficas con exudado purulento y petequias en paladar': ['faringe muy hiperémica, amígdalas hipertróficas con exudado purulento y petequias en paladar',
                                                                                                  'faringe intensamente eritematosa, amígdalas hipertróficas con exudado purulento y petequias en '
                                                                                                  'paladar',
                                                                                                  'amígdalas hipertróficas con exudado purulento, faringe muy hiperémica y petequias palatinas',
                                                                                                  'petequias en paladar, faringe muy hiperémica y amígdalas hipertróficas con exudado purulento',
                                                                                                  'hiperemia faríngea marcada, con hipertrofia amigdalina, exudado purulento y petequias en paladar'],
 'flujo vaginal grisáceo, homogéneo, fluido, de olor a pescado, adherido a las paredes vaginales, sin eritema marcado': ['flujo vaginal grisáceo, homogéneo, fluido, de olor a pescado, adherido a las '
                                                                                                                         'paredes vaginales, sin eritema marcado',
                                                                                                                         'flujo vaginal homogéneo, grisáceo y fluido, de olor a pescado, adherido a '
                                                                                                                         'las paredes vaginales, sin eritema marcado',
                                                                                                                         'secreción vaginal grisácea, homogénea y fluida, con olor a pescado, adherida '
                                                                                                                         'a las paredes vaginales, sin eritema marcado',
                                                                                                                         'leucorrea grisácea, homogénea, fluida, de olor a pescado, que se adhiere a '
                                                                                                                         'las paredes vaginales, sin eritema marcado',
                                                                                                                         'sin eritema marcado; flujo vaginal fluido, homogéneo y grisáceo, adherido a '
                                                                                                                         'las paredes vaginales, con olor a pescado'],
 'genitales externos sin alteraciones evidentes': ['genitales externos sin alteraciones evidentes',
                                                   'genitales externos de aspecto normal, sin alteraciones evidentes',
                                                   'sin alteraciones evidentes en genitales externos',
                                                   'genitales externos sin lesiones ni alteraciones evidentes',
                                                   'examen de genitales externos sin alteraciones aparentes'],
 'genitales externos sin alteraciones; sin lesiones ni signos de infección': ['genitales externos sin alteraciones; sin lesiones ni signos de infección',
                                                                              'genitales externos sin alteraciones, sin lesiones ni signos de infección',
                                                                              'sin lesiones ni signos de infección; genitales externos sin alteraciones',
                                                                              'genitales externos sin alteraciones evidentes, sin lesiones ni signos de infección',
                                                                              'genitales externos sin alteraciones, sin signos de infección ni lesiones'],
 'genitales externos sin lesiones ni signos de infección, sin secreción ni sangrado anormal': ['genitales externos sin lesiones ni signos de infección, sin secreción ni sangrado anormal',
                                                                                               'genitales externos sin lesiones ni datos de infección, sin flujo ni sangrado anormales',
                                                                                               'genitales externos de aspecto normal, sin signos de infección, sin secreción anormal ni sangrado',
                                                                                               'región genital externa sin lesiones, sin signos infecciosos y sin secreción ni sangrado fuera de lo '
                                                                                               'normal',
                                                                                               'sin lesiones ni signos de infección en genitales externos, ausencia de secreción y de sangrado '
                                                                                               'anormal'],
 'genitales externos sin lesiones; cuello uterino de aspecto normal si se explora': ['genitales externos sin lesiones; cuello uterino de aspecto normal si se explora',
                                                                                     'genitales externos sin lesiones; cuello uterino con aspecto normal si se explora',
                                                                                     'sin lesiones en genitales externos; si se explora, cuello uterino de aspecto normal',
                                                                                     'genitales externos sin lesiones, con cuello uterino de aspecto normal en caso de explorarse',
                                                                                     'cuello uterino de aspecto normal si se explora; genitales externos sin lesiones'],
 'glande y prepucio eritematosos, edematosos, con secreción blanquecina y erosiones': ['glande y prepucio eritematosos, edematosos, con secreción blanquecina y erosiones',
                                                                                       'glande y prepucio con eritema y edema, secreción blanquecina y erosiones',
                                                                                       'eritema y edema en glande y prepucio, con erosiones y secreción blanquecina',
                                                                                       'prepucio y glande eritematosos y edematosos, con erosiones y secreción blanquecina',
                                                                                       'glande y prepucio edematosos y eritematosos, con erosiones y secreción de aspecto blanquecino'],
 'habones eritematosos, pruriginosos y migratorios, de bordes bien definidos, con dermografismo y excoriaciones por rascado; sin edema de labios ni lengua y sin compromiso de la vía aérea': ['habones '
                                                                                                                                                                                               'eritematosos, '
                                                                                                                                                                                               'pruriginosos '
                                                                                                                                                                                               'y '
                                                                                                                                                                                               'migratorios, '
                                                                                                                                                                                               'de '
                                                                                                                                                                                               'bordes '
                                                                                                                                                                                               'bien '
                                                                                                                                                                                               'definidos, '
                                                                                                                                                                                               'con '
                                                                                                                                                                                               'dermografismo '
                                                                                                                                                                                               'y '
                                                                                                                                                                                               'excoriaciones '
                                                                                                                                                                                               'por '
                                                                                                                                                                                               'rascado; '
                                                                                                                                                                                               'sin '
                                                                                                                                                                                               'edema '
                                                                                                                                                                                               'de '
                                                                                                                                                                                               'labios '
                                                                                                                                                                                               'ni '
                                                                                                                                                                                               'lengua '
                                                                                                                                                                                               'y sin '
                                                                                                                                                                                               'compromiso '
                                                                                                                                                                                               'de la '
                                                                                                                                                                                               'vía '
                                                                                                                                                                                               'aérea',
                                                                                                                                                                                               'lesiones '
                                                                                                                                                                                               'habonosas '
                                                                                                                                                                                               'eritematosas, '
                                                                                                                                                                                               'pruriginosas '
                                                                                                                                                                                               'y de '
                                                                                                                                                                                               'carácter '
                                                                                                                                                                                               'migratorio, '
                                                                                                                                                                                               'con '
                                                                                                                                                                                               'bordes '
                                                                                                                                                                                               'bien '
                                                                                                                                                                                               'delimitados, '
                                                                                                                                                                                               'dermografismo '
                                                                                                                                                                                               'y '
                                                                                                                                                                                               'excoriaciones '
                                                                                                                                                                                               'por '
                                                                                                                                                                                               'rascado; '
                                                                                                                                                                                               'sin '
                                                                                                                                                                                               'edema '
                                                                                                                                                                                               'labial '
                                                                                                                                                                                               'ni '
                                                                                                                                                                                               'lingual '
                                                                                                                                                                                               'y con '
                                                                                                                                                                                               'vía '
                                                                                                                                                                                               'aérea '
                                                                                                                                                                                               'permeable',
                                                                                                                                                                                               'ronchas '
                                                                                                                                                                                               'eritematosas, '
                                                                                                                                                                                               'muy '
                                                                                                                                                                                               'pruriginosas, '
                                                                                                                                                                                               'migratorias '
                                                                                                                                                                                               'y de '
                                                                                                                                                                                               'bordes '
                                                                                                                                                                                               'netos, '
                                                                                                                                                                                               'con '
                                                                                                                                                                                               'dermografismo '
                                                                                                                                                                                               'positivo '
                                                                                                                                                                                               'y '
                                                                                                                                                                                               'excoriaciones '
                                                                                                                                                                                               'por '
                                                                                                                                                                                               'rascado; '
                                                                                                                                                                                               'labios '
                                                                                                                                                                                               'y '
                                                                                                                                                                                               'lengua '
                                                                                                                                                                                               'sin '
                                                                                                                                                                                               'edema, '
                                                                                                                                                                                               'sin '
                                                                                                                                                                                               'compromiso '
                                                                                                                                                                                               'de la '
                                                                                                                                                                                               'vía '
                                                                                                                                                                                               'aérea',
                                                                                                                                                                                               'habones '
                                                                                                                                                                                               'de '
                                                                                                                                                                                               'bordes '
                                                                                                                                                                                               'bien '
                                                                                                                                                                                               'definidos, '
                                                                                                                                                                                               'eritematosos, '
                                                                                                                                                                                               'pruriginosos '
                                                                                                                                                                                               'y que '
                                                                                                                                                                                               'migran, '
                                                                                                                                                                                               'con '
                                                                                                                                                                                               'dermografismo '
                                                                                                                                                                                               'y '
                                                                                                                                                                                               'huellas '
                                                                                                                                                                                               'de '
                                                                                                                                                                                               'rascado; '
                                                                                                                                                                                               'sin '
                                                                                                                                                                                               'angioedema '
                                                                                                                                                                                               'de '
                                                                                                                                                                                               'labios '
                                                                                                                                                                                               'o '
                                                                                                                                                                                               'lengua '
                                                                                                                                                                                               'ni '
                                                                                                                                                                                               'afectación '
                                                                                                                                                                                               'de la '
                                                                                                                                                                                               'vía '
                                                                                                                                                                                               'aérea',
                                                                                                                                                                                               'placas '
                                                                                                                                                                                               'urticarianas '
                                                                                                                                                                                               'eritematosas '
                                                                                                                                                                                               'y '
                                                                                                                                                                                               'pruriginosas, '
                                                                                                                                                                                               'migratorias, '
                                                                                                                                                                                               'de '
                                                                                                                                                                                               'bordes '
                                                                                                                                                                                               'definidos, '
                                                                                                                                                                                               'con '
                                                                                                                                                                                               'dermografismo '
                                                                                                                                                                                               'y '
                                                                                                                                                                                               'excoriaciones '
                                                                                                                                                                                               'por '
                                                                                                                                                                                               'rascado; '
                                                                                                                                                                                               'sin '
                                                                                                                                                                                               'edema '
                                                                                                                                                                                               'de '
                                                                                                                                                                                               'labios '
                                                                                                                                                                                               'ni '
                                                                                                                                                                                               'lengua, '
                                                                                                                                                                                               'con '
                                                                                                                                                                                               'vía '
                                                                                                                                                                                               'aérea '
                                                                                                                                                                                               'sin '
                                                                                                                                                                                               'compromiso'],
 'hematoma o aumento de volumen en región traumatizada, sin heridas penetrantes': ['hematoma o aumento de volumen en región traumatizada, sin heridas penetrantes',
                                                                                   'hematoma o aumento de volumen en la región traumatizada, sin heridas penetrantes',
                                                                                   'sin heridas penetrantes; hematoma o aumento de volumen en región traumatizada',
                                                                                   'región traumatizada con hematoma o aumento de volumen, sin heridas penetrantes',
                                                                                   'aumento de volumen o hematoma en el área del traumatismo, sin heridas penetrantes'],
 'herida con bordes irregulares, eritema perilesional, edema y secreción serosa o purulenta': ['herida con bordes irregulares, eritema perilesional, edema y secreción serosa o purulenta',
                                                                                               'herida de bordes irregulares con eritema perilesional, edema y secreción serosa o purulenta',
                                                                                               'herida con eritema perilesional y edema, de bordes irregulares, con secreción serosa o purulenta',
                                                                                               'solución de continuidad de bordes irregulares, con eritema perilesional, edema y secreción serosa o '
                                                                                               'purulenta',
                                                                                               'herida irregular en sus bordes, edematosa, con eritema alrededor y secreción serosa o purulenta'],
 'herida punzante o desgarro por mordedura con eritema, edema y dolor local': ['herida punzante o desgarro por mordedura con eritema, edema y dolor local',
                                                                               'herida punzante o desgarro por mordedura, con eritema, edema y dolor local',
                                                                               'eritema, edema y dolor local alrededor de herida punzante o desgarro por mordedura',
                                                                               'lesión por mordedura (herida punzante o desgarro) con eritema, edema y dolor en la zona',
                                                                               'herida por mordedura, punzante o con desgarro, con dolor local, eritema y edema'],
 'hipoacusia': ['hipoacusia', 'disminución de la agudeza auditiva', 'hipoacusia a la valoración clínica', 'audición disminuida', 'pérdida auditiva'],
 'inyección conjuntival periquerática, fotofobia y lagrimeo; agudeza visual disminuida': ['inyección conjuntival periquerática, fotofobia y lagrimeo; agudeza visual disminuida',
                                                                                          'inyección conjuntival periquerática con fotofobia y lagrimeo; agudeza visual disminuida',
                                                                                          'fotofobia, lagrimeo e inyección conjuntival periquerática; agudeza visual disminuida',
                                                                                          'agudeza visual disminuida; inyección conjuntival periquerática, fotofobia y lagrimeo',
                                                                                          'hiperemia conjuntival periquerática, con fotofobia, lagrimeo y disminución de la agudeza visual'],
 'lesiones anulares eritematosas con borde elevado y descamativo, centro más claro': ['lesiones anulares eritematosas con borde elevado y descamativo, centro más claro',
                                                                                      'lesiones eritematosas de forma anular, con borde elevado y descamativo y centro más claro',
                                                                                      'placas anulares con eritema, borde elevado con descamación y aclaramiento central',
                                                                                      'lesiones en anillo eritematosas, de borde elevado y descamativo, con centro más claro',
                                                                                      'lesiones anulares de borde elevado, eritematoso y descamativo, con centro de coloración más clara'],
 'lesiones de acné (comedones, pápulas y pústulas) en cara': ['lesiones de acné (comedones, pápulas y pústulas) en cara',
                                                              'lesiones acneicas (comedones, pápulas y pústulas) en la cara',
                                                              'comedones, pápulas y pústulas de acné en cara',
                                                              'acné facial con comedones, pápulas y pústulas',
                                                              'lesiones de acné en cara, con comedones, pápulas y pústulas'],
 'lesiones de acné en espalda y tórax': ['lesiones de acné en espalda y tórax',
                                         'lesiones acneicas en espalda y tórax',
                                         'acné en espalda y tórax',
                                         'lesiones de acné localizadas en espalda y tórax',
                                         'en espalda y tórax, lesiones de acné'],
 'lesiones eritematosas, pruriginosas y descamativas, con excoriaciones por rascado': ['lesiones eritematosas, pruriginosas y descamativas, con excoriaciones por rascado',
                                                                                       'lesiones eritematosas y descamativas, pruriginosas, con excoriaciones por rascado',
                                                                                       'lesiones pruriginosas, eritematosas y descamativas, acompañadas de excoriaciones por rascado',
                                                                                       'placas eritematosas con descamación y prurito, con excoriaciones secundarias al rascado',
                                                                                       'lesiones descamativas y eritematosas, con prurito y excoriaciones por rascado'],
 'lesiones erosivas con costras melicéricas (color miel) sobre base eritematosa': ['lesiones erosivas con costras melicéricas (color miel) sobre base eritematosa',
                                                                                   'erosiones con costras melicéricas (color miel) sobre una base eritematosa',
                                                                                   'costras melicéricas (color miel) sobre base eritematosa y lesiones erosivas',
                                                                                   'base eritematosa con lesiones erosivas cubiertas por costras de color miel (melicéricas)',
                                                                                   'lesiones erosivas y costrosas melicéricas (color miel) sobre piel eritematosa'],
 'lesiones papilomatosas, verrugosas, en forma de coliflor, en región genital y perianal': ['lesiones papilomatosas, verrugosas, en forma de coliflor, en región genital y perianal',
                                                                                            'lesiones verrugosas y papilomatosas en forma de coliflor en región genital y perianal',
                                                                                            'lesiones en forma de coliflor, papilomatosas y verrugosas, en región genital y perianal',
                                                                                            'en región genital y perianal, lesiones papilomatosas verrugosas con aspecto de coliflor',
                                                                                            'verrugas papilomatosas de aspecto en coliflor, en región genital y perianal'],
 'lesiones vesiculares en distintas etapas (máculas, pápulas, vesículas y costras) en cara, tronco y extremidades': ['lesiones vesiculares en distintas etapas (máculas, pápulas, vesículas y costras) '
                                                                                                                     'en cara, tronco y extremidades',
                                                                                                                     'lesiones en distintas etapas evolutivas (máculas, pápulas, vesículas y costras) '
                                                                                                                     'en cara, tronco y extremidades',
                                                                                                                     'en cara, tronco y extremidades, lesiones vesiculares en distintas etapas '
                                                                                                                     '(máculas, pápulas, vesículas y costras)',
                                                                                                                     'lesiones vesiculares polimorfas (máculas, pápulas, vesículas y costras) en '
                                                                                                                     'distintas etapas, en cara, tronco y extremidades',
                                                                                                                     'máculas, pápulas, vesículas y costras en distintas etapas de evolución, '
                                                                                                                     'distribuidas en cara, tronco y extremidades'],
 'lesiones vesiculopustulosas umbilicadas en distintas etapas': ['lesiones vesiculopustulosas umbilicadas en distintas etapas',
                                                                 'lesiones vesiculopustulosas con umbilicación, en distintas etapas',
                                                                 'lesiones umbilicadas vesiculopustulosas en distintas etapas evolutivas',
                                                                 'en distintas etapas, lesiones vesiculopustulosas umbilicadas',
                                                                 'lesiones vesiculopustulosas de centro umbilicado, en diferentes etapas'],
 'lesión en región anal, de bordes irregulares, dolorosa': ['lesión en región anal, de bordes irregulares, dolorosa',
                                                            'lesión dolorosa en región anal, de bordes irregulares',
                                                            'región anal con lesión de bordes irregulares y dolorosa',
                                                            'lesión anal dolorosa de bordes irregulares',
                                                            'en región anal, lesión de bordes irregulares, dolorosa a la palpación'],
 'lesión exofítica o ulcerada, friable, que sangra al contacto, de bordes irregulares; adenopatías inguinales': ['lesión exofítica o ulcerada, friable, que sangra al contacto, de bordes irregulares; '
                                                                                                                 'adenopatías inguinales',
                                                                                                                 'lesión exofítica o ulcerada, de bordes irregulares, friable y que sangra al '
                                                                                                                 'contacto; adenopatías inguinales',
                                                                                                                 'lesión friable, exofítica o ulcerada, de bordes irregulares, con sangrado al '
                                                                                                                 'contacto; con adenopatías inguinales',
                                                                                                                 'adenopatías inguinales; lesión exofítica o ulcerada, friable, de bordes irregulares, '
                                                                                                                 'que sangra al contacto',
                                                                                                                 'lesión de bordes irregulares, exofítica o ulcerada, friable, con sangrado al '
                                                                                                                 'contacto, y adenopatías inguinales'],
 'lesión nodular o elevada, bien delimitada, de crecimiento lento, móvil y no dolorosa': ['lesión nodular o elevada, bien delimitada, de crecimiento lento, móvil y no dolorosa',
                                                                                          'lesión elevada o nodular, bien delimitada, móvil, no dolorosa y de crecimiento lento',
                                                                                          'lesión bien delimitada, nodular o elevada, indolora, móvil y de crecimiento lento',
                                                                                          'nódulo o lesión elevada de bordes bien definidos, móvil, indolora y de lento crecimiento',
                                                                                          'lesión de crecimiento lento, nodular o elevada, bien delimitada, móvil y sin dolor'],
 'lesión nodular o pustulosa eritematosa, caliente, indurada y dolorosa a la palpación, con halo de eritema y, en ocasiones, fluctuación y drenaje purulento': ['lesión nodular o pustulosa '
                                                                                                                                                                'eritematosa, caliente, indurada y '
                                                                                                                                                                'dolorosa a la palpación, con halo de '
                                                                                                                                                                'eritema y, en ocasiones, fluctuación '
                                                                                                                                                                'y drenaje purulento',
                                                                                                                                                                'lesión nodular o pustulosa, '
                                                                                                                                                                'eritematosa, caliente, indurada y '
                                                                                                                                                                'dolorosa a la palpación, rodeada de '
                                                                                                                                                                'halo de eritema, con fluctuación y '
                                                                                                                                                                'drenaje purulento en ocasiones',
                                                                                                                                                                'lesión eritematosa nodular o '
                                                                                                                                                                'pustulosa, indurada, caliente y '
                                                                                                                                                                'dolorosa a la palpación, con halo '
                                                                                                                                                                'eritematoso y, en ocasiones, '
                                                                                                                                                                'fluctuación y salida de material '
                                                                                                                                                                'purulento',
                                                                                                                                                                'nódulo o pústula eritematosa, '
                                                                                                                                                                'caliente, indurada y dolorosa a la '
                                                                                                                                                                'palpación, con halo de eritema y, en '
                                                                                                                                                                'ocasiones, fluctuación y drenaje '
                                                                                                                                                                'purulento',
                                                                                                                                                                'lesión nodular o pustulosa caliente, '
                                                                                                                                                                'indurada, eritematosa y dolorosa a la '
                                                                                                                                                                'palpación, con eritema perilesional '
                                                                                                                                                                'en halo y, a veces, fluctuación con '
                                                                                                                                                                'drenaje purulento'],
 'lesión ulcerada o exofítica en orofaringe': ['lesión ulcerada o exofítica en orofaringe',
                                               'lesión exofítica o ulcerada en la orofaringe',
                                               'orofaringe con lesión ulcerada o exofítica',
                                               'en orofaringe, lesión exofítica o ulcerada',
                                               'presencia de lesión ulcerada o exofítica a nivel orofaríngeo'],
 'liendres y pediculos visibles en cuero cabelludo, con excoriaciones y costras en región occipital': ['liendres y pediculos visibles en cuero cabelludo, con excoriaciones y costras en región '
                                                                                                       'occipital',
                                                                                                       'pedículos y liendres visibles en cuero cabelludo, con excoriaciones y costras en región '
                                                                                                       'occipital',
                                                                                                       'cuero cabelludo con liendres y pediculos visibles; excoriaciones y costras en región occipital',
                                                                                                       'excoriaciones y costras en región occipital, con liendres y pediculos visibles en cuero '
                                                                                                       'cabelludo',
                                                                                                       'presencia de liendres y pediculos en cuero cabelludo, con costras y excoriaciones occipitales'],
 'mama con eritema, calor, induración y dolor a la palpación; sin zona fluctuante; adenopatías axilares dolorosas': ['mama con eritema, calor, induración y dolor a la palpación; sin zona fluctuante; '
                                                                                                                     'adenopatías axilares dolorosas',
                                                                                                                     'mama eritematosa, caliente, indurada y dolorosa a la palpación; sin zona '
                                                                                                                     'fluctuante; con adenopatías axilares dolorosas',
                                                                                                                     'mama con dolor a la palpación, eritema, calor e induración, sin zona fluctuante; '
                                                                                                                     'adenopatías axilares dolorosas',
                                                                                                                     'eritema, calor, induración y dolor a la palpación en la mama, sin zona '
                                                                                                                     'fluctuante, con adenopatías axilares dolorosas',
                                                                                                                     'adenopatías axilares dolorosas; mama con induración, eritema, calor y dolor a la '
                                                                                                                     'palpación, sin zona fluctuante'],
 'mamas con sensibilidad y nodularidad difusa': ['mamas con sensibilidad y nodularidad difusa',
                                                 'mamas con nodularidad difusa y sensibilidad',
                                                 'mamas sensibles, con nodularidad difusa',
                                                 'sensibilidad mamaria y nodularidad difusa',
                                                 'mamas con nodularidad difusa y dolor a la palpación'],
 'mamas simétricas, dolor a la palpación bilateral y sensibilidad difusa; sin masas, retracciones ni secreción por el pezón': ['mamas simétricas, dolor a la palpación bilateral y sensibilidad '
                                                                                                                               'difusa; sin masas, retracciones ni secreción por el pezón',
                                                                                                                               'mamas simétricas, con dolor a la palpación bilateral y sensibilidad '
                                                                                                                               'difusa; sin masas, retracciones ni secreción por el pezón',
                                                                                                                               'mamas simétricas con sensibilidad difusa y dolor bilateral a la '
                                                                                                                               'palpación, sin masas, retracciones ni secreción por el pezón',
                                                                                                                               'dolor a la palpación bilateral y sensibilidad difusa en mamas '
                                                                                                                               'simétricas; sin masas ni retracciones, sin secreción por el pezón',
                                                                                                                               'sin masas, retracciones ni secreción por el pezón; mamas simétricas, '
                                                                                                                               'con sensibilidad difusa y dolor bilateral a la palpación'],
 'masa mamaria dura, de bordes irregulares, adherida a planos, con retracción de piel o pezón y adenopatías axilares': ['masa mamaria dura, de bordes irregulares, adherida a planos, con retracción '
                                                                                                                        'de piel o pezón y adenopatías axilares',
                                                                                                                        'masa mamaria dura, de bordes irregulares, adherida a planos, con retracción '
                                                                                                                        'de la piel o del pezón y adenopatías axilares',
                                                                                                                        'masa dura en la mama, de bordes irregulares y adherida a planos, con '
                                                                                                                        'adenopatías axilares y retracción de piel o pezón',
                                                                                                                        'adenopatías axilares y masa mamaria dura de bordes irregulares, adherida a '
                                                                                                                        'planos, con retracción cutánea o del pezón',
                                                                                                                        'masa mamaria de consistencia dura, bordes irregulares y adherencia a planos, '
                                                                                                                        'con retracción de piel o pezón y adenopatías axilares'],
 'masa palpable en la mama, de bordes definidos, móvil, no adherida a planos profundos, sin cambios en la piel ni secreción por el pezón; sin adenopatías axilares': ['masa palpable en la mama, de '
                                                                                                                                                                      'bordes definidos, móvil, no '
                                                                                                                                                                      'adherida a planos profundos, '
                                                                                                                                                                      'sin cambios en la piel ni '
                                                                                                                                                                      'secreción por el pezón; sin '
                                                                                                                                                                      'adenopatías axilares',
                                                                                                                                                                      'masa mamaria palpable de bordes '
                                                                                                                                                                      'definidos, móvil y no adherida '
                                                                                                                                                                      'a planos profundos, sin cambios '
                                                                                                                                                                      'cutáneos ni secreción por el '
                                                                                                                                                                      'pezón; sin adenopatías axilares',
                                                                                                                                                                      'masa palpable en la mama, '
                                                                                                                                                                      'móvil, de bordes bien definidos '
                                                                                                                                                                      'y no adherida a planos '
                                                                                                                                                                      'profundos; piel sin cambios, '
                                                                                                                                                                      'sin secreción por el pezón ni '
                                                                                                                                                                      'adenopatías axilares',
                                                                                                                                                                      'sin adenopatías axilares, con '
                                                                                                                                                                      'masa mamaria palpable, móvil, '
                                                                                                                                                                      'de bordes definidos y no '
                                                                                                                                                                      'adherida a planos profundos, '
                                                                                                                                                                      'sin cambios en la piel ni '
                                                                                                                                                                      'secreción por el pezón',
                                                                                                                                                                      'tumoración mamaria palpable, '
                                                                                                                                                                      'bien delimitada, móvil, no '
                                                                                                                                                                      'adherida a planos profundos, '
                                                                                                                                                                      'sin alteraciones de la piel ni '
                                                                                                                                                                      'secreción por el pezón y sin '
                                                                                                                                                                      'adenopatías axilares'],
 'masa pálida, brillante y móvil que obstruye la fosa nasal': ['masa pálida, brillante y móvil que obstruye la fosa nasal',
                                                               'masa pálida, móvil y brillante que obstruye la fosa nasal',
                                                               'fosa nasal obstruida por masa pálida, brillante y móvil',
                                                               'masa móvil, pálida y brillante, que ocupa y obstruye la fosa nasal',
                                                               'obstrucción de la fosa nasal por masa brillante, pálida y móvil'],
 'masa reductible en región inguinal que aumenta con la maniobra de Valsalva, sin signos de estrangulamiento': ['masa reductible en región inguinal que aumenta con la maniobra de Valsalva, sin '
                                                                                                                'signos de estrangulamiento',
                                                                                                                'masa reductible en región inguinal que aumenta con la maniobra de Valsalva, sin datos '
                                                                                                                'de estrangulamiento',
                                                                                                                'sin signos de estrangulamiento, masa inguinal reductible que se acentúa con Valsalva',
                                                                                                                'tumoración inguinal reductible, que aumenta con la maniobra de Valsalva, sin signos '
                                                                                                                'de estrangulamiento',
                                                                                                                'abultamiento inguinal reductible que aumenta de tamaño con Valsalva, sin datos de '
                                                                                                                'estrangulamiento'],
 'membrana timpánica eritematosa, abombada y opaca, con disminución de la movilidad; otorrea si hay perforación': ['membrana timpánica eritematosa, abombada y opaca, con disminución de la movilidad; '
                                                                                                                   'otorrea si hay perforación',
                                                                                                                   'membrana timpánica hiperémica, abombada y opaca, con movilidad disminuida; otorrea '
                                                                                                                   'si hay perforación',
                                                                                                                   'tímpano eritematoso, abombado y opaco, con movilidad disminuida; otorrea en caso '
                                                                                                                   'de perforación',
                                                                                                                   'membrana timpánica opaca, abombada y eritematosa, con movilidad reducida; '
                                                                                                                   'presencia de otorrea si hay perforación',
                                                                                                                   'movilidad disminuida de la membrana timpánica, que se observa eritematosa, '
                                                                                                                   'abombada y opaca; otorrea si existe perforación'],
 'movimientos oculares alterados con limitación de la motilidad extrínseca y diplopía': ['movimientos oculares alterados con limitación de la motilidad extrínseca y diplopía',
                                                                                         'alteración de los movimientos oculares con limitación de la motilidad extrínseca y diplopía',
                                                                                         'diplopía con movimientos oculares alterados y limitación de la motilidad extrínseca',
                                                                                         'limitación de la motilidad ocular extrínseca con movimientos oculares alterados y diplopía',
                                                                                         'movimientos oculares anormales, con motilidad extrínseca limitada y diplopía'],
 'mucosa hiperémica con secreción mucopurulenta, dolor a la palpación de senos maxilares y frontales': ['mucosa hiperémica con secreción mucopurulenta, dolor a la palpación de senos maxilares y '
                                                                                                        'frontales',
                                                                                                        'mucosa eritematosa con secreción mucopurulenta, dolor a la palpación de senos maxilares y '
                                                                                                        'frontales',
                                                                                                        'secreción mucopurulenta sobre mucosa hiperémica, con dolor a la palpación de senos frontales '
                                                                                                        'y maxilares',
                                                                                                        'dolor a la palpación de senos maxilares y frontales, con mucosa hiperémica y secreción '
                                                                                                        'mucopurulenta',
                                                                                                        'mucosa nasal hiperémica con secreción mucopurulenta y dolorimiento a la palpación de senos '
                                                                                                        'maxilares y frontales'],
 'mucosa nasal pálida y edematosa, con rinorrea hialina y cornetes hipertróficos': ['mucosa nasal pálida y edematosa, con rinorrea hialina y cornetes hipertróficos',
                                                                                    'mucosa nasal pálida, edematosa, con rinorrea hialina y cornetes hipertróficos',
                                                                                    'cornetes hipertróficos con mucosa nasal pálida y edematosa y rinorrea hialina',
                                                                                    'rinorrea hialina, con mucosa nasal pálida y edematosa y cornetes hipertróficos',
                                                                                    'mucosa nasal de aspecto pálido y edematoso, con cornetes hipertróficos y secreción hialina'],
 'mucosa oral sin candidiasis': ['mucosa oral sin candidiasis',
                                 'sin candidiasis en la mucosa oral',
                                 'mucosa oral sin signos de candidiasis',
                                 'cavidad oral sin candidiasis',
                                 'sin placas de candidiasis en mucosa oral'],
 'mucosa vaginal pálida, delgada y seca, con atrofia vulvovaginal': ['mucosa vaginal pálida, delgada y seca, con atrofia vulvovaginal',
                                                                     'mucosa vaginal pálida, adelgazada y seca, con atrofia vulvovaginal',
                                                                     'atrofia vulvovaginal con mucosa vaginal pálida, delgada y seca',
                                                                     'atrofia vulvovaginal, con mucosa vaginal seca, delgada y pálida',
                                                                     'mucosa vaginal seca, pálida y delgada, con signos de atrofia vulvovaginal'],
 'murmullo vesicular conservado con roncus y estertores bronquiales dispersos, sin tiraje': ['murmullo vesicular conservado con roncus y estertores bronquiales dispersos, sin tiraje',
                                                                                             'murmullo vesicular conservado, con roncus y estertores bronquiales dispersos y sin tiraje',
                                                                                             'roncus y estertores bronquiales dispersos con murmullo vesicular conservado, sin tiraje',
                                                                                             'sin tiraje; murmullo vesicular conservado con roncus y estertores bronquiales dispersos',
                                                                                             'murmullo vesicular conservado, con estertores bronquiales y roncus dispersos, sin presencia de tiraje'],
 'murmullo vesicular conservado en ambos campos, sin ruidos agregados': ['murmullo vesicular conservado en ambos campos, sin ruidos agregados',
                                                                         'murmullo vesicular presente en ambos campos pulmonares, sin ruidos agregados',
                                                                         'campos pulmonares con murmullo vesicular conservado, sin estertores ni sibilancias',
                                                                         'sin ruidos agregados, con murmullo vesicular conservado bilateralmente',
                                                                         'ventilación bilateral conservada con murmullo vesicular normal, sin ruidos agregados'],
 'murmullo vesicular conservado, con estertores finos escasos o sin ruidos agregados; saturación de oxígeno a valorar': ['murmullo vesicular conservado, con estertores finos escasos o sin ruidos '
                                                                                                                         'agregados; saturación de oxígeno a valorar',
                                                                                                                         'murmullo vesicular conservado, con escasos estertores finos o sin ruidos '
                                                                                                                         'agregados; saturación de oxígeno a valorar',
                                                                                                                         'saturación de oxígeno a valorar; murmullo vesicular conservado, con '
                                                                                                                         'estertores finos escasos o sin ruidos agregados',
                                                                                                                         'murmullo vesicular conservado con estertores finos escasos o ausencia de '
                                                                                                                         'ruidos agregados; saturación de oxígeno por valorar',
                                                                                                                         'estertores finos escasos o sin ruidos agregados, con murmullo vesicular '
                                                                                                                         'conservado; saturación de oxígeno a valorar'],
 'murmullo vesicular conservado, sin ruidos agregados': ['murmullo vesicular conservado, sin ruidos agregados',
                                                         'murmullo vesicular conservado y sin ruidos agregados',
                                                         'sin ruidos agregados, con murmullo vesicular conservado',
                                                         'murmullo vesicular presente y conservado, sin ruidos agregados',
                                                         'ruidos respiratorios con murmullo vesicular conservado, sin ruidos agregados'],
 'máculas hipopigmentadas con descamación fina en tronco y cuello': ['máculas hipopigmentadas con descamación fina en tronco y cuello',
                                                                     'manchas hipopigmentadas con descamación fina en tronco y cuello',
                                                                     'descamación fina sobre máculas hipopigmentadas en tronco y cuello',
                                                                     'en tronco y cuello, máculas hipopigmentadas con fina descamación',
                                                                     'lesiones maculares hipocrómicas con descamación fina en tronco y cuello'],
 'máculas y nódulos violáceos en piel y mucosas': ['máculas y nódulos violáceos en piel y mucosas',
                                                   'nódulos y máculas violáceos en piel y mucosas',
                                                   'piel y mucosas con máculas y nódulos de coloración violácea',
                                                   'lesiones violáceas, maculares y nodulares, en piel y mucosas',
                                                   'presencia de máculas y nódulos violáceos en piel y en mucosas'],
 'nariz con fosas permeables, mucosa rosada y sin secreción': ['nariz con fosas permeables, mucosa rosada y sin secreción',
                                                               'fosas nasales permeables, con mucosa de coloración rosada y sin secreciones',
                                                               'nariz con mucosa rosada, fosas permeables y ausencia de secreción',
                                                               'mucosa nasal rosada, fosas nasales permeables, sin presencia de secreción',
                                                               'nariz de fosas permeables y mucosa rosada, sin rinorrea'],
 'nariz con mucosa hiperémica y edematosa, con rinorrea': ['nariz con mucosa hiperémica y edematosa, con rinorrea',
                                                           'nariz con mucosa edematosa e hiperémica, con rinorrea',
                                                           'nariz con rinorrea y mucosa hiperémica y edematosa',
                                                           'nariz con mucosa eritematosa y edematosa, con rinorrea',
                                                           'nariz con rinorrea, mucosa edematosa e hiperémica'],
 'no se explora de forma adecuada por falta de espacio clínico apropiado': ['no se explora de forma adecuada por falta de espacio clínico apropiado',
                                                                            'no se puede explorar adecuadamente por falta de espacio clínico apropiado',
                                                                            'exploración no adecuada por falta de espacio clínico apropiado',
                                                                            'no explorable de forma adecuada debido a la falta de espacio clínico apropiado',
                                                                            'no se logra una exploración adecuada por no contar con espacio clínico apropiado'],
 'normocéfala, sin masas ni lesiones': ['normocéfala, sin masas ni lesiones',
                                        'cráneo normocéfalo, sin masas ni lesiones',
                                        'sin masas ni lesiones, normocéfala',
                                        'cabeza normocéfala, sin lesiones ni masas palpables',
                                        'normocefalia, sin lesiones ni masas'],
 'nódulo firme e indoloro en el párpado, sin eritema marcado': ['nódulo firme e indoloro en el párpado, sin eritema marcado',
                                                                'nódulo firme, indoloro, en el párpado, sin eritema marcado',
                                                                'párpado con nódulo firme e indoloro, sin eritema marcado',
                                                                'nódulo palpebral firme e indoloro, sin eritema evidente',
                                                                'sin eritema marcado, con nódulo firme e indoloro en el párpado'],
 'ojos con pupilas isocóricas normorreactivas, conjuntivas rosadas y escleras anictéricas': ['ojos con pupilas isocóricas normorreactivas, conjuntivas rosadas y escleras anictéricas',
                                                                                             'ojos con conjuntivas rosadas, escleras anictéricas y pupilas isocóricas normorreactivas',
                                                                                             'ojos sin alteraciones: pupilas isocóricas y normorreactivas, escleras anictéricas, conjuntivas rosadas',
                                                                                             'ojos con escleras anictéricas, conjuntivas de coloración rosada y pupilas simétricas, normorreactivas a '
                                                                                             'la luz',
                                                                                             'ojos con pupilas simétricas y reactivas, sin ictericia escleral y con conjuntivas rosadas'],
 'ombligo con eritema periumbilical, secreción purulenta y mal olor': ['ombligo con eritema periumbilical, secreción purulenta y mal olor',
                                                                       'ombligo con secreción purulenta, mal olor y eritema periumbilical',
                                                                       'eritema periumbilical, con secreción purulenta y mal olor a nivel del ombligo',
                                                                       'ombligo con secreción purulenta fétida y eritema periumbilical',
                                                                       'región umbilical con eritema periumbilical, mal olor y secreción purulenta'],
 'opacidad del cristalino con disminución de la agudeza visual y reflejo pupilar conservado': ['opacidad del cristalino con disminución de la agudeza visual y reflejo pupilar conservado',
                                                                                               'cristalino opaco, con disminución de la agudeza visual y reflejo pupilar conservado',
                                                                                               'disminución de la agudeza visual con opacidad del cristalino; reflejo pupilar conservado',
                                                                                               'opacidad del cristalino, agudeza visual disminuida y reflejo pupilar conservado',
                                                                                               'reflejo pupilar conservado, con opacidad del cristalino y agudeza visual disminuida'],
 'orofaringe con hiperemia leve': ['orofaringe con hiperemia leve',
                                   'orofaringe levemente hiperémica',
                                   'hiperemia leve en la orofaringe',
                                   'orofaringe con leve eritema',
                                   'mucosa orofaríngea con hiperemia leve'],
 'orofaringe sin hiperemia ni exudado, amígdalas sin hipertrofia': ['orofaringe sin hiperemia ni exudado, amígdalas sin hipertrofia',
                                                                    'faringe sin hiperemia ni exudado, sin hipertrofia amigdalina',
                                                                    'orofaringe de aspecto normal, sin hiperemia, exudado ni hipertrofia amigdalina',
                                                                    'amígdalas sin hipertrofia, orofaringe sin hiperemia ni exudado',
                                                                    'mucosa orofaríngea sin eritema ni exudado y amígdalas de tamaño normal'],
 'oídos con conductos auditivos permeables y membranas timpánicas íntegras': ['oídos con conductos auditivos permeables y membranas timpánicas íntegras',
                                                                              'conductos auditivos externos permeables y membranas timpánicas íntegras en ambos oídos',
                                                                              'oídos con membranas timpánicas íntegras y conductos auditivos permeables',
                                                                              'oídos sin alteraciones, con conductos auditivos permeables y tímpanos íntegros',
                                                                              'ambos oídos con conductos auditivos externos libres y membranas timpánicas íntegras'],
 'oídos sin alteraciones; nistagmo horizontal-rotatorio, prueba de Dix-Hallpike positiva y marcha inestable': ['oídos sin alteraciones; nistagmo horizontal-rotatorio, prueba de Dix-Hallpike positiva '
                                                                                                               'y marcha inestable',
                                                                                                               'oídos sin alteraciones; con nistagmo horizontal-rotatorio, Dix-Hallpike positivo y '
                                                                                                               'marcha inestable',
                                                                                                               'oídos sin alteraciones; maniobra de Dix-Hallpike positiva, con nistagmo '
                                                                                                               'horizontal-rotatorio y marcha inestable',
                                                                                                               'sin alteraciones en oídos; marcha inestable, nistagmo horizontal-rotatorio y prueba de '
                                                                                                               'Dix-Hallpike positiva',
                                                                                                               'oídos sin hallazgos anormales; nistagmo horizontal-rotatorio, marcha inestable y '
                                                                                                               'Dix-Hallpike positivo'],
 'paciente alerta y colaboradora/o, con lenguaje expresivo disminuido y comprensión conservada': ['paciente alerta y colaboradora/o, con lenguaje expresivo disminuido y comprensión conservada',
                                                                                                  'paciente despierta/o y colaboradora/o, con disminución del lenguaje expresivo y comprensión '
                                                                                                  'conservada',
                                                                                                  'paciente alerta, colaboradora/o, con comprensión conservada y lenguaje expresivo disminuido',
                                                                                                  'paciente colaboradora/o y alerta, con comprensión del lenguaje conservada y expresión verbal '
                                                                                                  'disminuida',
                                                                                                  'paciente en estado de alerta, cooperadora/o, con habla expresiva pobre y comprensión adecuada'],
 'paciente ansiosa/o, con dolor': ['paciente ansiosa/o, con dolor',
                                   'paciente con dolor, ansiosa/o',
                                   'paciente ansiosa/o y con dolor',
                                   'paciente con dolor y ansiedad evidente',
                                   'paciente con expresión de dolor, ansiosa/o'],
 'paciente ansiosa/o, con facies de dolor y taquicardia leve': ['paciente ansiosa/o, con facies de dolor y taquicardia leve',
                                                                'paciente ansiosa/o, con gesto de dolor y frecuencia cardíaca ligeramente aumentada',
                                                                'paciente con facies álgica, ansiosa/o y con taquicardia leve',
                                                                'paciente inquieta/o, con expresión facial de dolor y discreta taquicardia',
                                                                'paciente con ansiedad, facies dolorosa y leve aumento de la frecuencia cardíaca'],
 'paciente ansiosa/o, con ánimo decaído': ['paciente ansiosa/o, con ánimo decaído',
                                           'paciente con ánimo decaído, ansiosa/o',
                                           'paciente ansiosa/o y de ánimo decaído',
                                           'paciente con ansiedad evidente y ánimo decaído',
                                           'paciente de ánimo decaído, con ansiedad'],
 'paciente ansiosa/o, inquieta/o, con taquicardia leve y sudoración palmar': ['paciente ansiosa/o, inquieta/o, con taquicardia leve y sudoración palmar',
                                                                              'paciente inquieta/o y ansiosa/o, con sudoración palmar y taquicardia leve',
                                                                              'paciente con ansiedad e inquietud, taquicardia leve y sudoración palmar',
                                                                              'paciente ansiosa/o, con inquietud, sudoración palmar y leve taquicardia',
                                                                              'paciente inquieta/o, ansiosa/o, que presenta taquicardia leve y sudoración palmar'],
 'paciente ansiosa/o, llorosa/o, con temor; se brinda espacio privado y confidencial': ['paciente ansiosa/o, llorosa/o, con temor; se brinda espacio privado y confidencial',
                                                                                        'paciente ansiosa/o, llorosa/o y con temor; se brinda un espacio privado y confidencial',
                                                                                        'paciente con temor, ansiosa/o y llorosa/o; se le brinda espacio privado y confidencial',
                                                                                        'se brinda espacio privado y confidencial a paciente ansiosa/o, llorosa/o y con temor',
                                                                                        'paciente llorosa/o, ansiosa/o y temerosa/o; se ofrece un espacio privado y confidencial'],
 'paciente con afecto aplanado, hipoprosexia y enlentecimiento psicomotor': ['paciente con afecto aplanado, hipoprosexia y enlentecimiento psicomotor',
                                                                             'paciente con afecto aplanado, hipoprosexia y lentitud psicomotora',
                                                                             'paciente con enlentecimiento psicomotor, hipoprosexia y afecto aplanado',
                                                                             'paciente con hipoprosexia, afecto aplanado y retardo psicomotor',
                                                                             'paciente con aplanamiento afectivo, hipoprosexia y enlentecimiento psicomotor'],
 'paciente con alteración del comportamiento y del juicio, colaboradora/o de forma parcial': ['paciente con alteración del comportamiento y del juicio, colaboradora/o de forma parcial',
                                                                                              'paciente con alteración del juicio y del comportamiento, parcialmente colaboradora/o',
                                                                                              'paciente colaboradora/o de forma parcial, con alteración del comportamiento y del juicio',
                                                                                              'paciente con juicio y comportamiento alterados, con colaboración parcial',
                                                                                              'paciente parcialmente colaboradora/o, con alteraciones del comportamiento y del juicio'],
 'paciente con bajo peso, disminución del tejido celular subcutáneo y masa muscular, y palidez': ['paciente con bajo peso, disminución del tejido celular subcutáneo y masa muscular, y palidez',
                                                                                                  'paciente con bajo peso, palidez y disminución del tejido celular subcutáneo y de la masa muscular',
                                                                                                  'paciente pálida/o, con bajo peso y disminución de masa muscular y del tejido celular subcutáneo',
                                                                                                  'bajo peso con palidez y pérdida del tejido celular subcutáneo y de la masa muscular',
                                                                                                  'paciente con palidez, bajo peso, masa muscular disminuida y escaso tejido celular subcutáneo'],
 'paciente con bochornos y sudoración': ['paciente con bochornos y sudoración',
                                         'paciente con sudoración y bochornos',
                                         'paciente que presenta bochornos y sudoración',
                                         'paciente con episodios de bochornos y sudoración',
                                         'paciente con sofocos y sudoración'],
 'paciente con cifras tensionales elevadas, edema palpebral y facial': ['paciente con cifras tensionales elevadas, edema palpebral y facial',
                                                                        'paciente con presión arterial elevada, edema palpebral y facial',
                                                                        'paciente con edema palpebral y facial y cifras tensionales elevadas',
                                                                        'paciente con cifras de presión arterial elevadas, con edema facial y palpebral',
                                                                        'paciente hipertensa/o, con edema en párpados y cara'],
 'paciente con facies de cansancio, ojeras y somnolencia diurna': ['paciente con facies de cansancio, ojeras y somnolencia diurna',
                                                                   'paciente con facies de cansancio, ojeras y somnolencia durante el día',
                                                                   'paciente somnolienta/o, con facies de cansancio y ojeras',
                                                                   'paciente con ojeras, facies de cansancio y somnolencia diurna',
                                                                   'paciente con somnolencia diurna, ojeras y facies de cansancio'],
 'paciente con fiebre y adenopatías': ['paciente con fiebre y adenopatías',
                                       'paciente febril, con adenopatías',
                                       'paciente con fiebre y ganglios linfáticos aumentados de tamaño',
                                       'paciente con adenopatías y fiebre',
                                       'paciente febril con linfadenopatías'],
 'paciente con mareo, sin déficit neurológico focal': ['paciente con mareo, sin déficit neurológico focal',
                                                       'paciente con mareo, sin focalización neurológica',
                                                       'paciente con sensación de mareo, sin déficit neurológico focal',
                                                       'sin déficit neurológico focal, paciente con mareo',
                                                       'paciente mareada/o, sin signos neurológicos focales'],
 'paciente con mucosas levemente secas': ['paciente con mucosas levemente secas',
                                          'paciente con leve sequedad de mucosas',
                                          'mucosas levemente secas en la/el paciente',
                                          'paciente con mucosas discretamente secas',
                                          'paciente que presenta mucosas ligeramente secas'],
 'paciente con mucosas secas, pérdida de peso y decaimiento': ['paciente con mucosas secas, pérdida de peso y decaimiento',
                                                               'paciente con decaimiento, pérdida de peso y mucosas secas',
                                                               'paciente con sequedad de mucosas, pérdida de peso y decaimiento',
                                                               'mucosas secas, con pérdida de peso y decaimiento en la/el paciente',
                                                               'paciente decaída/o, con pérdida de peso y mucosas secas'],
 'paciente con mucosas secas, turgencia de la piel disminuida, llenado capilar prolongado y ojos hundidos': ['paciente con mucosas secas, turgencia de la piel disminuida, llenado capilar prolongado '
                                                                                                             'y ojos hundidos',
                                                                                                             'paciente con mucosas secas, ojos hundidos, turgencia de la piel disminuida y llenado '
                                                                                                             'capilar prolongado',
                                                                                                             'mucosas secas, turgencia cutánea disminuida, llenado capilar prolongado y ojos hundidos '
                                                                                                             'en la paciente',
                                                                                                             'paciente con ojos hundidos, mucosas secas, llenado capilar prolongado y disminución de '
                                                                                                             'la turgencia de la piel',
                                                                                                             'paciente con signos de deshidratación: mucosas secas, ojos hundidos, turgencia de la '
                                                                                                             'piel disminuida y llenado capilar prolongado'],
 'paciente con obesidad, IMC elevado, acantosis nigricans a valorar': ['paciente con obesidad, IMC elevado, acantosis nigricans a valorar',
                                                                       'paciente con obesidad e IMC elevado, con acantosis nigricans a valorar',
                                                                       'paciente con IMC elevado y obesidad; acantosis nigricans a valorar',
                                                                       'paciente obesa/o, IMC elevado, a valorar acantosis nigricans',
                                                                       'paciente con obesidad, con IMC elevado y acantosis nigricans por valorar'],
 'paciente con palidez cutáneo-mucosa': ['paciente con palidez cutáneo-mucosa',
                                         'paciente con palidez de piel y mucosas',
                                         'palidez cutáneo-mucosa evidente en la/el paciente',
                                         'paciente pálida/o a nivel de piel y mucosas',
                                         'paciente que presenta palidez en piel y mucosas'],
 'paciente con palidez de piel y mucosas, taquicárdica leve': ['paciente con palidez de piel y mucosas, taquicárdica leve',
                                                               'paciente con palidez cutáneo-mucosa y taquicardia leve',
                                                               'paciente con piel y mucosas pálidas, levemente taquicárdica/o',
                                                               'paciente levemente taquicárdica/o, con palidez de piel y mucosas',
                                                               'paciente con palidez generalizada de piel y mucosas y taquicardia leve'],
 'paciente con palidez y edema palpebral': ['paciente con palidez y edema palpebral',
                                            'paciente con palidez y edema en los párpados',
                                            'paciente pálida/o, con edema palpebral',
                                            'edema palpebral y palidez en la/el paciente',
                                            'paciente que presenta edema palpebral y palidez'],
 'paciente con rasgos físicos que sugieren alteración del desarrollo, a valorar': ['paciente con rasgos físicos que sugieren alteración del desarrollo, a valorar',
                                                                                   'paciente con características físicas sugestivas de trastorno del desarrollo, a valorar',
                                                                                   'paciente con fenotipo que sugiere alteración del desarrollo, pendiente de valoración',
                                                                                   'paciente con hallazgos físicos compatibles con posible alteración del desarrollo, a valorar',
                                                                                   'paciente que presenta rasgos físicos sugerentes de un trastorno del desarrollo, por valorar'],
 'paciente con sobrepeso; sin xantomas ni xantelasmas': ['paciente con sobrepeso; sin xantomas ni xantelasmas',
                                                         'paciente con sobrepeso, sin xantomas ni xantelasmas',
                                                         'sobrepeso, sin presencia de xantomas ni xantelasmas',
                                                         'paciente con exceso de peso; no se observan xantomas ni xantelasmas',
                                                         'sin xantomas ni xantelasmas; paciente con sobrepeso'],
 'paciente con tendencia a la hipotensión ortostática': ['paciente con tendencia a la hipotensión ortostática',
                                                         'paciente con tendencia a presentar hipotensión ortostática',
                                                         'paciente con hipotensión ortostática tendencial',
                                                         'paciente propensa/o a la hipotensión ortostática',
                                                         'paciente que tiende a la hipotensión ortostática'],
 'paciente con tinte ictérico en piel': ['paciente con tinte ictérico en piel',
                                         'paciente con piel de tinte ictérico',
                                         'paciente con coloración ictérica de la piel',
                                         'tinte ictérico cutáneo en la/el paciente',
                                         'paciente con ictericia cutánea'],
 'paciente consciente, orientada/o, Glasgow 15 puntos': ['paciente consciente, orientada/o, Glasgow 15 puntos',
                                                         'paciente consciente y orientada/o, con Glasgow de 15 puntos',
                                                         'paciente orientada/o, consciente, escala de Glasgow 15/15',
                                                         'paciente alerta, orientada/o, con puntuación de Glasgow de 15',
                                                         'paciente consciente, orientada/o, con Glasgow 15/15 puntos'],
 'paciente consciente, orientada/o, hidratada/o, afebril y en aceptable estado general': ['paciente consciente, orientada/o, hidratada/o, afebril y en aceptable estado general',
                                                                                          'paciente consciente y orientada/o, hidratada/o, afebril y en aceptable estado general',
                                                                                          'paciente alerta, orientada/o, bien hidratada/o, afebril y en aceptables condiciones generales',
                                                                                          'paciente en aceptable estado general, consciente, orientada/o, con adecuada hidratación y sin fiebre',
                                                                                          'paciente afebril, hidratada/o, consciente y orientada/o, con aceptable estado general'],
 'paciente en aceptable estado general, con cifras de presión arterial elevadas': ['paciente en aceptable estado general, con cifras de presión arterial elevadas',
                                                                                   'paciente con cifras de presión arterial elevadas, en aceptable estado general',
                                                                                   'paciente en aceptable estado general, con presión arterial elevada',
                                                                                   'en aceptable estado general, con cifras tensionales elevadas',
                                                                                   'paciente con aceptable estado general y cifras de presión arterial elevadas'],
 'paciente en aceptable estado general, con facies de molestia y dolor abdominal referido, sin datos de abdomen agudo': ['paciente en aceptable estado general, con facies de molestia y dolor '
                                                                                                                         'abdominal referido, sin datos de abdomen agudo',
                                                                                                                         'paciente en aceptables condiciones generales, con gesto de molestia, que '
                                                                                                                         'refiere dolor abdominal, sin datos de abdomen agudo',
                                                                                                                         'paciente con aceptable estado general, facies de incomodidad y dolor '
                                                                                                                         'abdominal referido, sin signos de abdomen agudo',
                                                                                                                         'paciente en aceptable estado general, con expresión de molestia y dolor '
                                                                                                                         'abdominal referido, sin evidencia de abdomen agudo',
                                                                                                                         'paciente en buen estado general, con facies de malestar y dolor abdominal '
                                                                                                                         'referido, sin datos que sugieran abdomen agudo'],
 'paciente en aceptable estado general, con fiebre': ['paciente en aceptable estado general, con fiebre',
                                                      'paciente con fiebre y aceptable estado general',
                                                      'paciente febril, en aceptable estado general',
                                                      'paciente en aceptable estado general, con elevación de la temperatura corporal',
                                                      'paciente con aceptable estado general, cursando con fiebre'],
 'paciente en aceptable estado general, con fiebre baja': ['paciente en aceptable estado general, con fiebre baja',
                                                           'paciente en aceptable estado general, con febrícula',
                                                           'paciente con aceptable estado general y fiebre de bajo grado',
                                                           'paciente en aceptable estado general, con elevación leve de la temperatura',
                                                           'paciente con fiebre baja y aceptable estado general'],
 'paciente en aceptable estado general, con ganancia de peso acorde': ['paciente en aceptable estado general, con ganancia de peso acorde',
                                                                       'paciente en aceptable estado general, con ganancia ponderal acorde',
                                                                       'paciente en aceptables condiciones generales, con ganancia de peso acorde',
                                                                       'paciente con aceptable estado general y ganancia de peso acorde',
                                                                       'paciente con ganancia de peso acorde, en aceptable estado general'],
 'paciente en aceptable estado general, con mucosas orales levemente secas y sin datos de deshidratación severa': ['paciente en aceptable estado general, con mucosas orales levemente secas y sin '
                                                                                                                   'datos de deshidratación severa',
                                                                                                                   'paciente en aceptables condiciones generales, con mucosa oral ligeramente seca, '
                                                                                                                   'sin signos de deshidratación severa',
                                                                                                                   'paciente con aceptable estado general, mucosas orales discretamente secas y sin '
                                                                                                                   'datos de deshidratación grave',
                                                                                                                   'paciente en aceptable estado general, con leve sequedad de mucosas orales, sin '
                                                                                                                   'signos de deshidratación severa',
                                                                                                                   'paciente en buen estado general, mucosas orales algo secas, sin evidencia de '
                                                                                                                   'deshidratación severa'],
 'paciente en aceptable estado general, con pérdida de peso a valorar': ['paciente en aceptable estado general, con pérdida de peso a valorar',
                                                                         'paciente con pérdida de peso a valorar, en aceptable estado general',
                                                                         'paciente en aceptable estado general; pérdida de peso por valorar',
                                                                         'en aceptable estado general, con posible pérdida de peso a valorar',
                                                                         'paciente con aceptable estado general y pérdida de peso a valorar'],
 'paciente en aceptable estado general, con signos vitales estables y sin datos de compromiso hemodinámico': ['paciente en aceptable estado general, con signos vitales estables y sin datos de '
                                                                                                              'compromiso hemodinámico',
                                                                                                              'paciente en aceptables condiciones generales, signos vitales estables, sin datos de '
                                                                                                              'compromiso hemodinámico',
                                                                                                              'paciente con aceptable estado general, hemodinámicamente estable y con signos vitales '
                                                                                                              'estables',
                                                                                                              'paciente en aceptable estado general, signos vitales dentro de parámetros estables, sin '
                                                                                                              'evidencia de compromiso hemodinámico',
                                                                                                              'paciente en buen estado general, con constantes vitales estables y sin signos de '
                                                                                                              'compromiso hemodinámico'],
 'paciente en aceptable estado general, febril, con malestar general': ['paciente en aceptable estado general, febril, con malestar general',
                                                                        'paciente febril, con malestar general y aceptable estado general',
                                                                        'paciente en aceptable estado general, con fiebre y malestar general',
                                                                        'paciente con malestar general y fiebre, en aceptable estado general',
                                                                        'paciente febril y con malestar general, en aceptable estado general'],
 'paciente en aceptable estado general, que refiere ardor o dolor epigástrico, sin datos de deshidratación': ['paciente en aceptable estado general, que refiere ardor o dolor epigástrico, sin datos '
                                                                                                              'de deshidratación',
                                                                                                              'paciente en aceptables condiciones generales, que refiere dolor o ardor en epigastrio, '
                                                                                                              'sin signos de deshidratación',
                                                                                                              'paciente con aceptable estado general, refiere ardor o dolor epigástrico y no presenta '
                                                                                                              'datos de deshidratación',
                                                                                                              'paciente en aceptable estado general, con ardor o dolor epigástrico referido, sin '
                                                                                                              'evidencia de deshidratación',
                                                                                                              'paciente en buen estado general, que refiere dolor o ardor epigástrico, hidratada/o y '
                                                                                                              'sin signos de deshidratación'],
 'paciente en aceptable estado general, sin datos de infección activa': ['paciente en aceptable estado general, sin datos de infección activa',
                                                                         'paciente en aceptables condiciones generales, sin signos de infección activa',
                                                                         'paciente con aceptable estado general y sin evidencia de infección activa',
                                                                         'paciente en aceptable estado general, afebril y sin datos de proceso infeccioso activo',
                                                                         'paciente en buen estado general, sin signos clínicos de infección activa'],
 'paciente en aceptable estado general, sin signos de descompensación aguda, con piel y mucosas hidratadas': ['paciente en aceptable estado general, sin signos de descompensación aguda, con piel y '
                                                                                                              'mucosas hidratadas',
                                                                                                              'paciente en aceptables condiciones generales, sin datos de descompensación aguda, piel '
                                                                                                              'y mucosas hidratadas',
                                                                                                              'paciente con aceptable estado general, piel y mucosas hidratadas, sin signos de '
                                                                                                              'descompensación aguda',
                                                                                                              'paciente en aceptable estado general, con adecuada hidratación de piel y mucosas y sin '
                                                                                                              'datos de descompensación aguda',
                                                                                                              'paciente en buen estado general, sin evidencia de descompensación aguda, con piel y '
                                                                                                              'mucosas bien hidratadas'],
 'paciente en buen estado general, activo, con peso y talla acordes para la edad': ['paciente en buen estado general, activo, con peso y talla acordes para la edad',
                                                                                    'paciente activo/a, en buen estado general, con peso y talla acordes a la edad',
                                                                                    'paciente en buenas condiciones generales, activo/a, con peso y talla adecuados para la edad',
                                                                                    'paciente con buen estado general, activo/a, y peso y talla acordes para su edad',
                                                                                    'paciente activo/a y en buen estado general, con peso y talla acordes con la edad'],
 'paciente en buen estado general, con peso y talla acordes': ['paciente en buen estado general, con peso y talla acordes',
                                                               'paciente en buen estado general, con peso y talla acordes a lo esperado',
                                                               'paciente con peso y talla acordes, en buen estado general',
                                                               'paciente en buen estado general, con adecuado peso y talla',
                                                               'paciente con buen estado general y parámetros de peso y talla acordes'],
 'paciente en regular estado general, con pérdida de peso y palidez': ['paciente en regular estado general, con pérdida de peso y palidez',
                                                                       'paciente con pérdida de peso y palidez, en regular estado general',
                                                                       'paciente en regular estado general, pálida/o y con pérdida de peso',
                                                                       'paciente con regular estado general, palidez y pérdida ponderal',
                                                                       'paciente pálida/o, con pérdida de peso y regular estado general'],
 'paciente febril, con escalofríos, palidez y esplenomegalia a valorar': ['paciente febril, con escalofríos, palidez y esplenomegalia a valorar',
                                                                          'paciente febril, con escalofríos y palidez; esplenomegalia a valorar',
                                                                          'paciente con fiebre, escalofríos, palidez y esplenomegalia por valorar',
                                                                          'esplenomegalia a valorar; paciente febril, con escalofríos y palidez',
                                                                          'paciente con fiebre y escalofríos, pálida/o, con esplenomegalia a valorar'],
 'paciente febril, con malestar general, astenia y tos': ['paciente febril, con malestar general, astenia y tos',
                                                          'paciente con fiebre, malestar general, astenia y tos',
                                                          'paciente febril con astenia, malestar general y tos',
                                                          'paciente con tos, fiebre, astenia y malestar general',
                                                          'paciente febril, asténica/o, con malestar general y tos'],
 'paciente febril, con malestar general, dolor retroocular y mialgias': ['paciente febril, con malestar general, dolor retroocular y mialgias',
                                                                         'paciente con fiebre, malestar general, dolor retroocular y mialgias',
                                                                         'paciente febril que presenta mialgias, dolor retroocular y malestar general',
                                                                         'paciente con malestar general y fiebre, con dolor retroocular y mialgias',
                                                                         'paciente febril, con mialgias, malestar general y dolor retroocular'],
 'paciente febril, con polipnea y aspecto de enfermedad': ['paciente febril, con polipnea y aspecto de enfermedad',
                                                           'paciente con fiebre, polipnea y aspecto de enfermedad',
                                                           'paciente febril, polipneica y de aspecto enfermo',
                                                           'paciente con aspecto de enfermedad, febril y con polipnea',
                                                           'paciente con polipnea, fiebre y aspecto de enfermedad'],
 'paciente inquieta/o, con dolor intenso': ['paciente inquieta/o, con dolor intenso',
                                            'paciente con dolor intenso, inquieta/o',
                                            'paciente con inquietud psicomotora y dolor intenso',
                                            'paciente con dolor de gran intensidad, inquieta/o',
                                            'paciente inquieta/o y con dolor intenso'],
 'paciente irritable': ['paciente irritable', 'paciente con irritabilidad', 'paciente de humor irritable', 'paciente que se muestra irritable', 'paciente con estado de ánimo irritable'],
 'paciente pálida, con taquicardia leve': ['paciente pálida, con taquicardia leve',
                                           'paciente con palidez y taquicardia leve',
                                           'paciente pálida y con taquicardia leve',
                                           'paciente con taquicardia leve, pálida',
                                           'paciente con palidez cutánea y leve taquicardia'],
 'paciente somnolienta/o o en periodo postcrítico, sin déficit neurológico focal': ['paciente somnolienta/o o en periodo postcrítico, sin déficit neurológico focal',
                                                                                    'paciente somnolienta/o o en periodo poscrítico, sin focalización neurológica',
                                                                                    'paciente en periodo postcrítico o somnolienta/o, sin déficit neurológico focal',
                                                                                    'sin déficit neurológico focal, paciente somnolienta/o o en periodo postcrítico',
                                                                                    'paciente con somnolencia o en fase postcrítica, sin signos neurológicos focales'],
 'paciente sudorosa/o, con temblor y palidez': ['paciente sudorosa/o, con temblor y palidez',
                                                'paciente con sudoración, temblor y palidez',
                                                'paciente pálida/o, sudorosa/o y con temblor',
                                                'paciente con temblor, palidez y diaforesis',
                                                'paciente con diaforesis, palidez y temblor'],
 'placa eritematosa, caliente, edematosa y dolorosa, de bordes mal definidos, con aumento de volumen del segmento afectado; adenopatías regionales dolorosas': ['placa eritematosa, caliente, '
                                                                                                                                                                'edematosa y dolorosa, de bordes mal '
                                                                                                                                                                'definidos, con aumento de volumen del '
                                                                                                                                                                'segmento afectado; adenopatías '
                                                                                                                                                                'regionales dolorosas',
                                                                                                                                                                'placa de eritema, calor, edema y '
                                                                                                                                                                'dolor, con bordes mal definidos y '
                                                                                                                                                                'aumento de volumen del segmento '
                                                                                                                                                                'afectado; con adenopatías regionales '
                                                                                                                                                                'dolorosas',
                                                                                                                                                                'segmento afectado aumentado de '
                                                                                                                                                                'volumen, con placa eritematosa, '
                                                                                                                                                                'edematosa, caliente y dolorosa de '
                                                                                                                                                                'bordes mal delimitados; adenopatías '
                                                                                                                                                                'regionales dolorosas',
                                                                                                                                                                'placa caliente, eritematosa, '
                                                                                                                                                                'edematosa y dolorosa a la palpación, '
                                                                                                                                                                'de límites mal definidos, con aumento '
                                                                                                                                                                'de volumen del segmento afectado; '
                                                                                                                                                                'adenopatías regionales dolorosas',
                                                                                                                                                                'eritema, calor, edema y dolor en '
                                                                                                                                                                'placa de bordes imprecisos con '
                                                                                                                                                                'aumento de volumen del segmento '
                                                                                                                                                                'afectado; se palpan adenopatías '
                                                                                                                                                                'regionales dolorosas'],
 'placas blanquecinas removibles en lengua y mucosa oral': ['placas blanquecinas removibles en lengua y mucosa oral',
                                                            'placas blanquecinas en lengua y mucosa oral, removibles',
                                                            'lengua y mucosa oral con placas blanquecinas que se desprenden',
                                                            'mucosa oral y lengua con placas removibles de color blanquecino',
                                                            'presencia de placas blanquecinas removibles en mucosa oral y lengua'],
 'prepucio que no logra retraerse, con edema y eritema; en parafimosis, glande edematoso y doloroso': ['prepucio que no logra retraerse, con edema y eritema; en parafimosis, glande edematoso y '
                                                                                                       'doloroso',
                                                                                                       'prepucio no retráctil, con edema y eritema; en parafimosis, glande edematoso y doloroso',
                                                                                                       'imposibilidad para retraer el prepucio, con edema y eritema; en caso de parafimosis, glande '
                                                                                                       'edematoso y doloroso',
                                                                                                       'prepucio con edema y eritema que no se retrae; en parafimosis, glande doloroso y edematoso',
                                                                                                       'prepucio que no se puede retraer, con eritema y edema; si hay parafimosis, glande edematoso y '
                                                                                                       'doloroso'],
 'pulsos distales disminuidos o ausentes, piel fría, pálida y con disminución del vello; llenado capilar prolongado': ['pulsos distales disminuidos o ausentes, piel fría, pálida y con disminución '
                                                                                                                       'del vello; llenado capilar prolongado',
                                                                                                                       'pulsos distales disminuidos o ausentes, piel fría, pálida y con menos vello, '
                                                                                                                       'con llenado capilar prolongado',
                                                                                                                       'disminución o ausencia de pulsos distales, con piel fría, pálida y con pérdida '
                                                                                                                       'de vello; llenado capilar prolongado',
                                                                                                                       'piel fría, pálida y con disminución del vello, llenado capilar prolongado y '
                                                                                                                       'pulsos distales débiles o ausentes',
                                                                                                                       'llenado capilar prolongado, pulsos distales disminuidos o ausentes, piel '
                                                                                                                       'pálida, fría y con hipotricosis'],
 'puño percusión lumbar negativa': ['puño percusión lumbar negativa',
                                    'puñopercusión lumbar negativa',
                                    'signo de puñopercusión lumbar negativo bilateral',
                                    'sin dolor a la puñopercusión lumbar',
                                    'puño percusión lumbar bilateral negativa'],
 'puño percusión lumbar negativa o dolorosa si hay compromiso alto': ['puño percusión lumbar negativa o dolorosa si hay compromiso alto',
                                                                      'puño percusión lumbar negativa, o dolorosa si hay compromiso alto',
                                                                      'puño percusión lumbar negativa; dolorosa en caso de compromiso alto',
                                                                      'puñopercusión lumbar negativa o dolorosa en caso de compromiso alto',
                                                                      'prueba de puño percusión lumbar negativa o dolorosa si existe compromiso alto'],
 'puño percusión lumbar positiva del lado afectado': ['puño percusión lumbar positiva del lado afectado',
                                                      'puño percusión lumbar positiva en el lado afectado',
                                                      'puño percusión positiva en la región lumbar del lado afectado',
                                                      'signo de puño percusión lumbar positivo del lado afectado',
                                                      'puño percusión del lado afectado positiva en región lumbar'],
 'pápulas excoriadas y trayectos lineales en espacios interdigitales y muñecas, con costras por rascado': ['pápulas excoriadas y trayectos lineales en espacios interdigitales y muñecas, con costras '
                                                                                                           'por rascado',
                                                                                                           'pápulas con excoriaciones y trayectos lineales en espacios interdigitales y muñecas, con '
                                                                                                           'costras secundarias al rascado',
                                                                                                           'en espacios interdigitales y muñecas, pápulas excoriadas y trayectos lineales, con costras '
                                                                                                           'por rascado',
                                                                                                           'trayectos lineales y pápulas excoriadas en muñecas y espacios interdigitales, con costras '
                                                                                                           'por rascado',
                                                                                                           'pápulas excoriadas, trayectos lineales y costras por rascado en espacios interdigitales y '
                                                                                                           'muñecas'],
 'pápulas hiperqueratósicas, rugosas e indoloras en dorso de manos y dedos': ['pápulas hiperqueratósicas, rugosas e indoloras en dorso de manos y dedos',
                                                                              'pápulas rugosas, hiperqueratósicas e indoloras en el dorso de las manos y los dedos',
                                                                              'en dorso de manos y dedos, pápulas hiperqueratósicas, rugosas e indoloras',
                                                                              'lesiones papulares hiperqueratósicas, rugosas e indoloras localizadas en dorso de manos y dedos',
                                                                              'dorso de manos y dedos con pápulas indoloras, rugosas e hiperqueratósicas'],
 'pápulas pequeñas, color piel, perladas, con umbilicación central': ['pápulas pequeñas, color piel, perladas, con umbilicación central',
                                                                      'pápulas pequeñas, perladas, de color piel, con umbilicación central',
                                                                      'pápulas color piel, pequeñas y perladas, con umbilicación en el centro',
                                                                      'pápulas de pequeño tamaño, perladas, color piel, con depresión umbilicada central',
                                                                      'pápulas perladas, color piel y pequeñas, con umbilicación central'],
 'párpado eritematoso, edematoso y doloroso, con nódulo con punto purulento en el borde': ['párpado eritematoso, edematoso y doloroso, con nódulo con punto purulento en el borde',
                                                                                           'párpado con eritema, edema y dolor, con nódulo que presenta punto purulento en el borde',
                                                                                           'nódulo en el borde palpebral con punto purulento, con párpado eritematoso, edematoso y doloroso',
                                                                                           'párpado doloroso, eritematoso y edematoso, con nódulo de punto purulento en el borde',
                                                                                           'borde palpebral con nódulo y punto purulento, con eritema, edema y dolor del párpado'],
 'quemadura de espesor parcial con eritema, flictenas y dolor intenso': ['quemadura de espesor parcial con eritema, flictenas y dolor intenso',
                                                                         'quemadura de segundo grado superficial con eritema, flictenas y dolor intenso',
                                                                         'lesión por quemadura de espesor parcial, eritematosa, con flictenas y dolor intenso',
                                                                         'eritema con flictenas y dolor intenso compatibles con quemadura de espesor parcial',
                                                                         'área de quemadura de espesor parcial con flictenas, eritema y dolor intenso'],
 'recién nacido activo, reactivo': ['recién nacido activo, reactivo',
                                    'recién nacido reactivo, activo',
                                    'recién nacido con actividad y reactividad adecuadas',
                                    'recién nacido activo y reactivo',
                                    'recién nacido que se muestra activo, reactivo al estímulo'],
 'recién nacido en regular estado general, con peso bajo y llanto débil, ictericia en cara y tronco si procede': ['recién nacido en regular estado general, con peso bajo y llanto débil, ictericia en '
                                                                                                                  'cara y tronco si procede',
                                                                                                                  'recién nacido en regular estado general, con bajo peso y llanto débil, con '
                                                                                                                  'ictericia en cara y tronco si procede',
                                                                                                                  'recién nacido con peso bajo y llanto débil, en regular estado general; ictericia en '
                                                                                                                  'cara y tronco si procede',
                                                                                                                  'recién nacido en regular estado general, llanto débil y bajo peso, con ictericia '
                                                                                                                  'facial y troncal si procede',
                                                                                                                  'recién nacido de bajo peso, en regular estado general, con llanto débil e ictericia '
                                                                                                                  'en cara y tronco si procede'],
 'región anal con hemorroides externas o prolapsadas, fisura o plexos hemorroidales dolorosos; tacto rectal con sangre en el dedo de guante': ['región anal con hemorroides externas o prolapsadas, '
                                                                                                                                               'fisura o plexos hemorroidales dolorosos; tacto rectal '
                                                                                                                                               'con sangre en el dedo de guante',
                                                                                                                                               'región anal con hemorroides externas o prolapsadas, '
                                                                                                                                               'fisura o plexos hemorroidales dolorosos; sangre en el '
                                                                                                                                               'dedo de guante al tacto rectal',
                                                                                                                                               'hemorroides externas o prolapsadas, fisura o plexos '
                                                                                                                                               'hemorroidales dolorosos en región anal; tacto rectal '
                                                                                                                                               'con sangre en el dedo de guante',
                                                                                                                                               'tacto rectal con sangre en el dedo de guante; región '
                                                                                                                                               'anal con hemorroides externas o prolapsadas, fisura o '
                                                                                                                                               'plexos hemorroidales dolorosos',
                                                                                                                                               'región anal con plexos hemorroidales dolorosos, '
                                                                                                                                               'externos o prolapsados, o fisura; sangre en el dedo de '
                                                                                                                                               'guante al tacto rectal'],
 'ruidos cardíacos arrítmicos o taquicárdicos, sin soplos': ['ruidos cardíacos arrítmicos o taquicárdicos, sin soplos',
                                                             'ruidos cardíacos arrítmicos o taquicárdicos, sin soplos audibles',
                                                             'sin soplos, con ruidos cardíacos arrítmicos o taquicárdicos',
                                                             'ruidos cardíacos taquicárdicos o arrítmicos, sin soplos',
                                                             'ruidos cardíacos con arritmia o taquicardia, sin soplos'],
 'ruidos cardíacos rítmicos, con posible desdoblamiento o soplo sistólico suave': ['ruidos cardíacos rítmicos, con posible desdoblamiento o soplo sistólico suave',
                                                                                   'ruidos cardíacos rítmicos, con posible desdoblamiento o soplo sistólico de baja intensidad',
                                                                                   'ruidos rítmicos con posible desdoblamiento o soplo sistólico suave',
                                                                                   'ruidos cardíacos rítmicos; posible soplo sistólico suave o desdoblamiento',
                                                                                   'ritmo cardíaco regular, con posible desdoblamiento de los ruidos o soplo sistólico suave'],
 'ruidos cardíacos rítmicos, de buena intensidad, sin soplos': ['ruidos cardíacos rítmicos, de buena intensidad, sin soplos',
                                                                'ruidos cardíacos de buena intensidad y rítmicos, sin presencia de soplos',
                                                                'latidos cardíacos rítmicos, con ruidos de buena intensidad y sin soplos',
                                                                'ruidos cardíacos rítmicos y bien audibles, sin soplos agregados',
                                                                'corazón con ruidos rítmicos de buena intensidad, sin soplos audibles'],
 'ruidos cardíacos rítmicos, sin soplos; frecuencia cardíaca normal': ['ruidos cardíacos rítmicos, sin soplos; frecuencia cardíaca normal',
                                                                       'ruidos cardíacos rítmicos, sin soplos, con frecuencia cardíaca normal',
                                                                       'frecuencia cardíaca normal, con ruidos cardíacos rítmicos y sin soplos',
                                                                       'ruidos cardíacos rítmicos y sin soplos; frecuencia cardíaca dentro de límites normales',
                                                                       'ritmo cardíaco regular, sin soplos, con frecuencia cardíaca normal'],
 'ruidos respiratorios con roncus escasos': ['ruidos respiratorios con roncus escasos',
                                             'ruidos respiratorios con escasos roncus',
                                             'roncus escasos a la auscultación de los ruidos respiratorios',
                                             'ruidos respiratorios acompañados de roncus escasos',
                                             'a la auscultación, escasos roncus con ruidos respiratorios presentes'],
 'sangrado vaginal escaso o abundante con coágulos; cuello uterino sin lesiones; útero de tamaño normal, no doloroso': ['sangrado vaginal escaso o abundante con coágulos; cuello uterino sin '
                                                                                                                        'lesiones; útero de tamaño normal, no doloroso',
                                                                                                                        'sangrado vaginal escaso o abundante con coágulos; cérvix sin lesiones; útero '
                                                                                                                        'de tamaño normal y no doloroso',
                                                                                                                        'cuello uterino sin lesiones, con sangrado vaginal escaso o abundante con '
                                                                                                                        'coágulos; útero de tamaño normal, no doloroso',
                                                                                                                        'útero de tamaño normal, no doloroso; cuello uterino sin lesiones y sangrado '
                                                                                                                        'vaginal escaso o abundante con coágulos',
                                                                                                                        'hemorragia vaginal escasa o abundante con coágulos; cuello uterino sin '
                                                                                                                        'lesiones, útero de tamaño normal e indoloro'],
 'sangrado vaginal escaso o moderado de color rojo oscuro; cuello uterino cerrado; útero acorde a la edad gestacional': ['sangrado vaginal escaso o moderado de color rojo oscuro; cuello uterino '
                                                                                                                         'cerrado; útero acorde a la edad gestacional',
                                                                                                                         'sangrado vaginal escaso o moderado, rojo oscuro; cuello uterino cerrado; '
                                                                                                                         'útero acorde a la edad gestacional',
                                                                                                                         'cuello uterino cerrado, con sangrado vaginal escaso o moderado de color rojo '
                                                                                                                         'oscuro; útero acorde a la edad gestacional',
                                                                                                                         'sangrado vaginal de cantidad escasa a moderada y color rojo oscuro; cérvix '
                                                                                                                         'cerrado; útero acorde a la edad gestacional',
                                                                                                                         'útero acorde a la edad gestacional; cuello uterino cerrado y sangrado '
                                                                                                                         'vaginal escaso o moderado de color rojo oscuro'],
 'se valora únicamente con su consentimiento': ['se valora únicamente con su consentimiento',
                                                'se explora únicamente con su consentimiento',
                                                'valoración realizada solo con su consentimiento',
                                                'se valora solo si la paciente lo consiente',
                                                'exploración condicionada a su consentimiento'],
 'secreción anormal o lesiones genitales, adenopatías inguinales; a valorar según el caso': ['secreción anormal o lesiones genitales, adenopatías inguinales; a valorar según el caso',
                                                                                             'secreción anormal o lesiones genitales y adenopatías inguinales; a valorar según el caso',
                                                                                             'lesiones genitales o secreción anormal, con adenopatías inguinales; a valorar según el caso',
                                                                                             'adenopatías inguinales y secreción anormal o lesiones genitales; por valorar según el caso',
                                                                                             'a valorar según el caso: secreción anormal o lesiones genitales, con adenopatías inguinales'],
 'secreción láctea bilateral a la expresión de los pezones; sin masas': ['secreción láctea bilateral a la expresión de los pezones; sin masas',
                                                                         'secreción láctea bilateral a la expresión de ambos pezones; sin masas',
                                                                         'a la expresión de los pezones, secreción láctea bilateral; sin masas',
                                                                         'sin masas; salida bilateral de secreción láctea a la expresión de los pezones',
                                                                         'expresión de los pezones con secreción láctea en ambas mamas, sin masas'],
 'secreción mucopurulenta por el orificio cervical, cuello uterino eritematoso y friable, con sangrado al contacto; dolor leve a la movilización cervical': ['secreción mucopurulenta por el orificio '
                                                                                                                                                             'cervical, cuello uterino eritematoso y '
                                                                                                                                                             'friable, con sangrado al contacto; dolor '
                                                                                                                                                             'leve a la movilización cervical',
                                                                                                                                                             'secreción mucopurulenta por el orificio '
                                                                                                                                                             'cervical, cuello uterino hiperémico y '
                                                                                                                                                             'friable, con sangrado al contacto; dolor '
                                                                                                                                                             'leve a la movilización cervical',
                                                                                                                                                             'cuello uterino eritematoso y friable que '
                                                                                                                                                             'sangra al contacto, con secreción '
                                                                                                                                                             'mucopurulenta por el orificio cervical; '
                                                                                                                                                             'dolor leve a la movilización cervical',
                                                                                                                                                             'dolor leve a la movilización cervical, '
                                                                                                                                                             'con secreción mucopurulenta por el '
                                                                                                                                                             'orificio cervical y cuello uterino '
                                                                                                                                                             'eritematoso, friable y con sangrado al '
                                                                                                                                                             'contacto',
                                                                                                                                                             'flujo mucopurulento por el orificio '
                                                                                                                                                             'cervical, cérvix eritematoso y friable '
                                                                                                                                                             'con sangrado al contacto; leve dolor a '
                                                                                                                                                             'la movilización cervical'],
 'sensibilidad conservada o disminuida en monofilamento, pulsos distales presentes, sin úlceras': ['sensibilidad conservada o disminuida en monofilamento, pulsos distales presentes, sin úlceras',
                                                                                                   'pulsos distales presentes, sin úlceras, con sensibilidad al monofilamento conservada o disminuida',
                                                                                                   'sin úlceras; sensibilidad conservada o disminuida al monofilamento y pulsos distales presentes',
                                                                                                   'sensibilidad al monofilamento conservada o disminuida, con pulsos distales presentes y ausencia de '
                                                                                                   'úlceras',
                                                                                                   'ausencia de úlceras, pulsos distales presentes y sensibilidad conservada o disminuida con '
                                                                                                   'monofilamento'],
 'sibilancias espiratorias difusas, espiración prolongada': ['sibilancias espiratorias difusas, espiración prolongada',
                                                             'espiración prolongada con sibilancias espiratorias difusas',
                                                             'sibilancias difusas durante la espiración, con espiración prolongada',
                                                             'sibilancias espiratorias diseminadas y espiración prolongada',
                                                             'espiración prolongada y sibilancias difusas en la fase espiratoria'],
 'sibilancias y crepitantes finos difusos con espiración prolongada': ['sibilancias y crepitantes finos difusos con espiración prolongada',
                                                                       'sibilancias y estertores crepitantes finos difusos, con espiración prolongada',
                                                                       'espiración prolongada con sibilancias y crepitantes finos difusos',
                                                                       'crepitantes finos y sibilancias difusos, con fase espiratoria prolongada',
                                                                       'estertores crepitantes finos y sibilancias en forma difusa, con espiración prolongada'],
 'simétricas, sin edema ni deformidades, con movilidad y fuerza conservadas, llenado capilar menor de 2 segundos': ['simétricas, sin edema ni deformidades, con movilidad y fuerza conservadas, '
                                                                                                                    'llenado capilar menor de 2 segundos',
                                                                                                                    'simétricas, sin edema ni deformidades, con fuerza y movilidad conservadas y '
                                                                                                                    'llenado capilar menor de 2 segundos',
                                                                                                                    'sin edema ni deformidades, simétricas, con llenado capilar menor de 2 segundos, '
                                                                                                                    'movilidad y fuerza conservadas',
                                                                                                                    'extremidades simétricas, sin deformidades ni edema, con llenado capilar menor de '
                                                                                                                    '2 segundos y fuerza y movilidad conservadas',
                                                                                                                    'simétricas, con movilidad y fuerza conservadas, sin edema ni deformidades, y '
                                                                                                                    'llenado capilar menor de 2 segundos'],
 'simétrico': ['simétrico', 'tórax simétrico', 'de configuración simétrica', 'simétrico a la inspección', 'tórax de aspecto simétrico'],
 'simétrico, con buena expansibilidad y sin tiraje': ['simétrico, con buena expansibilidad y sin tiraje',
                                                      'tórax simétrico, con adecuada expansibilidad y sin tiraje',
                                                      'simétrico, sin tiraje y con buena expansibilidad',
                                                      'de configuración simétrica, expansibilidad conservada y sin tiraje',
                                                      'simétrico, con expansión torácica adecuada, sin tiraje intercostal ni subcostal'],
 'simétrico, con uso leve de músculos accesorios si hay crisis': ['simétrico, con uso leve de músculos accesorios si hay crisis',
                                                                  'simétrico, con leve uso de músculos accesorios si hay crisis',
                                                                  'simétrico; en caso de crisis, leve uso de musculatura accesoria',
                                                                  'simétrico, con discreta utilización de músculos accesorios durante la crisis',
                                                                  'simétrico, con uso leve de musculatura accesoria en caso de crisis'],
 'simétrico, móvil, sin adenopatías ni masas, tiroides no palpable, sin ingurgitación yugular': ['simétrico, móvil, sin adenopatías ni masas, tiroides no palpable, sin ingurgitación yugular',
                                                                                                 'simétrico y móvil, sin masas ni adenopatías palpables, sin ingurgitación yugular y con tiroides no '
                                                                                                 'palpable',
                                                                                                 'sin masas ni adenopatías, simétrico, con movilidad conservada, tiroides no palpable y sin '
                                                                                                 'ingurgitación yugular',
                                                                                                 'móvil y simétrico, tiroides no palpable, sin ingurgitación yugular, sin adenopatías ni masas',
                                                                                                 'sin ingurgitación yugular, simétrico, móvil, sin adenopatías ni masas y con tiroides no palpable'],
 'sin dolor a la palpación de la pared torácica': ['sin dolor a la palpación de la pared torácica',
                                                   'pared torácica sin dolor a la palpación',
                                                   'no hay dolor a la palpación de la pared torácica',
                                                   'la palpación de la pared torácica no produce dolor',
                                                   'pared torácica indolora a la palpación'],
 'sin edema significativo ni várices': ['sin edema significativo ni várices',
                                        'sin várices ni edema significativo',
                                        'no se observa edema significativo ni várices',
                                        'ausencia de edema significativo y de várices',
                                        'sin presencia de várices ni edema significativo'],
 'sin lesiones; dolor a la palpación de musculatura pericraneal y temporal, sin signos meníngeos': ['sin lesiones; dolor a la palpación de musculatura pericraneal y temporal, sin signos meníngeos',
                                                                                                    'sin lesiones, con dolor a la palpación de la musculatura pericraneal y temporal; sin signos '
                                                                                                    'meníngeos',
                                                                                                    'dolor a la palpación de musculatura pericraneal y temporal, sin lesiones ni signos meníngeos',
                                                                                                    'sin signos meníngeos; sin lesiones, con dolor a la palpación de la musculatura temporal y '
                                                                                                    'pericraneal',
                                                                                                    'sin lesiones evidentes, con musculatura pericraneal y temporal dolorosa a la palpación y sin '
                                                                                                    'signos meníngeos'],
 'tacto bimanual con útero aumentado de tamaño, irregular, de consistencia firme, no doloroso': ['tacto bimanual con útero aumentado de tamaño, irregular, de consistencia firme, no doloroso',
                                                                                                 'al tacto bimanual, útero aumentado de tamaño, irregular, de consistencia firme y no doloroso',
                                                                                                 'tacto bimanual con útero de tamaño aumentado, contorno irregular, consistencia firme, sin dolor',
                                                                                                 'útero aumentado de tamaño, irregular y firme al tacto bimanual, no doloroso',
                                                                                                 'tacto bimanual: útero irregular, de consistencia firme, aumentado de tamaño y no doloroso'],
 'tacto rectal con próstata aumentada de tamaño, de consistencia elástica y con o sin dolor, sin nódulos duros': ['tacto rectal con próstata aumentada de tamaño, de consistencia elástica y con o sin '
                                                                                                                  'dolor, sin nódulos duros',
                                                                                                                  'tacto rectal con próstata de tamaño aumentado, consistencia elástica, con o sin '
                                                                                                                  'dolor y sin nódulos duros',
                                                                                                                  'próstata aumentada de tamaño al tacto rectal, de consistencia elástica, con o sin '
                                                                                                                  'dolor, sin nódulos duros',
                                                                                                                  'al tacto rectal, próstata agrandada de consistencia elástica, con o sin dolor y sin '
                                                                                                                  'presencia de nódulos duros',
                                                                                                                  'tacto rectal sin nódulos duros, con próstata aumentada de tamaño y consistencia '
                                                                                                                  'elástica, con o sin dolor'],
 'temblor de reposo, rigidez en rueda dentada y bradicinesia; marcha con pasos cortos': ['temblor de reposo, rigidez en rueda dentada y bradicinesia; marcha con pasos cortos',
                                                                                         'temblor de reposo, bradicinesia y rigidez en rueda dentada; marcha con pasos cortos',
                                                                                         'rigidez en rueda dentada, temblor de reposo y bradicinesia; marcha de pasos cortos',
                                                                                         'marcha con pasos cortos; temblor de reposo, rigidez en rueda dentada y bradicinesia',
                                                                                         'bradicinesia con temblor de reposo y rigidez en rueda dentada; marcha de pasos cortos'],
 'tiraje subcostal e intercostal, aleteo nasal': ['tiraje subcostal e intercostal, aleteo nasal',
                                                  'tiraje intercostal y subcostal, con aleteo nasal',
                                                  'aleteo nasal y tiraje subcostal e intercostal',
                                                  'presencia de tiraje subcostal e intercostal y aleteo nasal',
                                                  'aleteo nasal con tiraje intercostal y subcostal'],
 'tiroides palpable o no, sin nódulos; sin adenopatías': ['tiroides palpable o no, sin nódulos; sin adenopatías',
                                                          'tiroides palpable o no, sin nódulos, y sin adenopatías',
                                                          'sin adenopatías; tiroides palpable o no, sin nódulos',
                                                          'sin nódulos tiroideos, tiroides palpable o no; sin adenopatías',
                                                          'tiroides sin nódulos, palpable o no, y sin adenopatías cervicales'],
 'uñas engrosadas, amarillentas, quebradizas, con onicólisis': ['uñas engrosadas, amarillentas, quebradizas, con onicólisis',
                                                                'uñas amarillentas, engrosadas y quebradizas, con onicólisis',
                                                                'uñas con engrosamiento, coloración amarillenta, fragilidad y onicólisis',
                                                                'uñas quebradizas, engrosadas y amarillentas, con onicólisis',
                                                                'onicólisis con uñas engrosadas, amarillentas y quebradizas'],
 'vesículas agrupadas sobre base eritematosa con distribución unilateral en dermatoma, con costras y dolor a la palpación': ['vesículas agrupadas sobre base eritematosa con distribución unilateral '
                                                                                                                             'en dermatoma, con costras y dolor a la palpación',
                                                                                                                             'vesículas agrupadas sobre base eritematosa, de distribución unilateral '
                                                                                                                             'en dermatoma, con costras y dolor a la palpación',
                                                                                                                             'lesiones vesiculares agrupadas sobre base eritematosa siguiendo un '
                                                                                                                             'dermatoma unilateral, con costras y dolorosas a la palpación',
                                                                                                                             'distribución dermatomal unilateral de vesículas agrupadas sobre base '
                                                                                                                             'eritematosa, con costras y dolor a la palpación',
                                                                                                                             'vesículas y costras agrupadas sobre base eritematosa en dermatoma '
                                                                                                                             'unilateral, dolorosas a la palpación'],
 'vesículas agrupadas sobre base eritematosa en labio, con costras': ['vesículas agrupadas sobre base eritematosa en labio, con costras',
                                                                      'vesículas agrupadas en labio sobre base eritematosa, con costras',
                                                                      'en labio, vesículas agrupadas con base eritematosa y costras',
                                                                      'lesiones vesiculares agrupadas sobre base eritematosa en labio, con costras',
                                                                      'labio con vesículas agrupadas, base eritematosa y presencia de costras'],
 'vesículas agrupadas y úlceras superficiales dolorosas sobre base eritematosa en región genital, con adenopatías inguinales dolorosas': ['vesículas agrupadas y úlceras superficiales dolorosas sobre '
                                                                                                                                          'base eritematosa en región genital, con adenopatías '
                                                                                                                                          'inguinales dolorosas',
                                                                                                                                          'región genital con vesículas agrupadas y úlceras '
                                                                                                                                          'superficiales dolorosas sobre base eritematosa, con '
                                                                                                                                          'adenopatías inguinales dolorosas',
                                                                                                                                          'úlceras superficiales dolorosas y vesículas agrupadas sobre '
                                                                                                                                          'base eritematosa en región genital, con adenopatías '
                                                                                                                                          'inguinales dolorosas',
                                                                                                                                          'adenopatías inguinales dolorosas, con vesículas agrupadas y '
                                                                                                                                          'úlceras superficiales dolorosas de base eritematosa en '
                                                                                                                                          'región genital',
                                                                                                                                          'en región genital, vesículas agrupadas y úlceras '
                                                                                                                                          'superficiales dolorosas con base eritematosa, y adenopatías '
                                                                                                                                          'dolorosas inguinales'],
 'vulva con excoriaciones por rascado, eritema leve y liquenificación': ['vulva con excoriaciones por rascado, eritema leve y liquenificación',
                                                                         'vulva con eritema leve, excoriaciones por rascado y liquenificación',
                                                                         'excoriaciones por rascado en la vulva, con eritema leve y liquenificación',
                                                                         'vulva con liquenificación, excoriaciones por rascado y leve eritema',
                                                                         'eritema leve y liquenificación vulvar, con excoriaciones por rascado'],
 'vulva eritematosa y edematosa con fisuras; leucorrea blanquecina, espesa, grumosa, adherida a las paredes vaginales, sin mal olor': ['vulva eritematosa y edematosa con fisuras; leucorrea '
                                                                                                                                       'blanquecina, espesa, grumosa, adherida a las paredes '
                                                                                                                                       'vaginales, sin mal olor',
                                                                                                                                       'vulva eritematosa y edematosa con fisuras; flujo blanquecino, '
                                                                                                                                       'espeso, grumoso, adherido a las paredes vaginales, sin mal '
                                                                                                                                       'olor',
                                                                                                                                       'vulva edematosa y eritematosa con fisuras; secreción vaginal '
                                                                                                                                       'blanquecina, espesa, grumosa, adherida a las paredes '
                                                                                                                                       'vaginales, sin mal olor',
                                                                                                                                       'leucorrea blanquecina, espesa y grumosa, adherida a las '
                                                                                                                                       'paredes vaginales y sin mal olor; vulva eritematosa y '
                                                                                                                                       'edematosa con fisuras',
                                                                                                                                       'vulva con eritema, edema y fisuras; leucorrea grumosa, espesa '
                                                                                                                                       'y blanquecina, adherida a las paredes vaginales, inodora'],
 'vulva eritematosa y edematosa; flujo vaginal amarillento, purulento, fétido y abundante, con eritema de las paredes vaginales y cuello uterino': ['vulva eritematosa y edematosa; flujo vaginal '
                                                                                                                                                    'amarillento, purulento, fétido y abundante, con '
                                                                                                                                                    'eritema de las paredes vaginales y cuello uterino',
                                                                                                                                                    'vulva edematosa y eritematosa; flujo vaginal '
                                                                                                                                                    'abundante, purulento, amarillento y fétido, con '
                                                                                                                                                    'eritema de las paredes vaginales y del cuello '
                                                                                                                                                    'uterino',
                                                                                                                                                    'flujo vaginal purulento, amarillento, fétido y '
                                                                                                                                                    'abundante; vulva eritematosa y edematosa, con '
                                                                                                                                                    'eritema de paredes vaginales y cuello uterino',
                                                                                                                                                    'vulva con eritema y edema; leucorrea amarillenta, '
                                                                                                                                                    'purulenta, fétida y abundante, con paredes '
                                                                                                                                                    'vaginales y cuello uterino eritematosos',
                                                                                                                                                    'secreción vaginal amarillenta, purulenta, fétida '
                                                                                                                                                    'y abundante, con vulva eritematosa y edematosa y '
                                                                                                                                                    'eritema de paredes vaginales y cuello uterino'],
 'vulva eritematosa, edematosa y dolorosa, con fisuras o excoriaciones y flujo escaso': ['vulva eritematosa, edematosa y dolorosa, con fisuras o excoriaciones y flujo escaso',
                                                                                         'vulva eritematosa, edematosa y dolorosa, con fisuras o excoriaciones y leucorrea escasa',
                                                                                         'vulva dolorosa, eritematosa y edematosa, con excoriaciones o fisuras y secreción escasa',
                                                                                         'flujo escaso; vulva eritematosa, edematosa y dolorosa, con fisuras o excoriaciones',
                                                                                         'vulva con eritema, edema y dolor, con excoriaciones o fisuras y flujo vaginal escaso'],
 'área de picadura con eritema, edema y dolor local, parestesias en la zona': ['área de picadura con eritema, edema y dolor local, parestesias en la zona',
                                                                               'área de picadura con eritema, edema y dolor local, con parestesias en la zona',
                                                                               'zona de picadura eritematosa, edematosa y dolorosa, con parestesias locales',
                                                                               'eritema, edema y dolor local en el área de picadura, con parestesias en la zona',
                                                                               'área de la picadura con dolor local, eritema y edema, y parestesias en la región'],
 'úlcera con bordes irregulares, fondo con tejido de granulación o fibrina, secreción y eritema perilesional; pulsos distales disminuidos': ['úlcera con bordes irregulares, fondo con tejido de '
                                                                                                                                             'granulación o fibrina, secreción y eritema perilesional; '
                                                                                                                                             'pulsos distales disminuidos',
                                                                                                                                             'úlcera de bordes irregulares, con fondo de tejido de '
                                                                                                                                             'granulación o fibrina, secreción y eritema perilesional; '
                                                                                                                                             'pulsos distales disminuidos',
                                                                                                                                             'úlcera con secreción, eritema perilesional y bordes '
                                                                                                                                             'irregulares, fondo con granulación o fibrina; pulsos '
                                                                                                                                             'distales disminuidos',
                                                                                                                                             'pulsos distales disminuidos; úlcera de bordes '
                                                                                                                                             'irregulares con fondo de fibrina o tejido de '
                                                                                                                                             'granulación, secreción y eritema perilesional',
                                                                                                                                             'úlcera irregular en sus bordes, con fondo de granulación '
                                                                                                                                             'o fibrina, con secreción y eritema alrededor de la '
                                                                                                                                             'lesión; pulsos distales disminuidos'],
 'úlceras redondeadas con halo eritematoso y fondo blanquecino en mucosa oral, dolorosas': ['úlceras redondeadas con halo eritematoso y fondo blanquecino en mucosa oral, dolorosas',
                                                                                            'úlceras dolorosas, redondeadas, con halo eritematoso y fondo blanquecino en la mucosa oral',
                                                                                            'mucosa oral con úlceras redondeadas dolorosas, de fondo blanquecino y halo eritematoso',
                                                                                            'lesiones ulceradas redondeadas en mucosa oral, dolorosas, con fondo blanquecino y halo eritematoso',
                                                                                            'en mucosa oral, úlceras dolorosas de forma redondeada con fondo blanquecino rodeado de halo eritematoso'],
 'útero gestante acorde a la edad gestacional': ['útero gestante acorde a la edad gestacional',
                                                 'útero gestante con tamaño acorde a la edad gestacional',
                                                 'útero gestante de tamaño acorde a las semanas de gestación',
                                                 'altura uterina acorde a la edad gestacional',
                                                 'útero grávido acorde a la edad gestacional'],
 'útero gestante con altura uterina acorde a la edad gestacional, frecuencia cardíaca fetal presente y sin sangrado ni pérdida de líquido': ['útero gestante con altura uterina acorde a la edad '
                                                                                                                                             'gestacional, frecuencia cardíaca fetal presente y sin '
                                                                                                                                             'sangrado ni pérdida de líquido',
                                                                                                                                             'útero gestante con altura uterina acorde a la edad '
                                                                                                                                             'gestacional, con frecuencia cardíaca fetal presente, sin '
                                                                                                                                             'sangrado ni pérdida de líquido',
                                                                                                                                             'frecuencia cardíaca fetal presente, altura uterina '
                                                                                                                                             'acorde a la edad gestacional, sin sangrado ni pérdida de '
                                                                                                                                             'líquido',
                                                                                                                                             'altura uterina acorde a la edad gestacional en útero '
                                                                                                                                             'gestante, con frecuencia cardíaca fetal presente; sin '
                                                                                                                                             'sangrado ni salida de líquido',
                                                                                                                                             'útero gestante con altura uterina acorde a las semanas '
                                                                                                                                             'de gestación, latido cardíaco fetal presente, sin '
                                                                                                                                             'sangrado ni pérdida de líquido'],
 'útero involucionando, a nivel infraumbilical, loquios en cantidad y aspecto normales; herida quirúrgica o episiorrafia sin signos de infección': ['útero involucionando, a nivel infraumbilical, '
                                                                                                                                                    'loquios en cantidad y aspecto normales; herida '
                                                                                                                                                    'quirúrgica o episiorrafia sin signos de infección',
                                                                                                                                                    'útero en involución, a nivel infraumbilical, con '
                                                                                                                                                    'loquios de cantidad y aspecto normales; herida '
                                                                                                                                                    'quirúrgica o episiorrafia sin signos de infección',
                                                                                                                                                    'loquios en cantidad y aspecto normales, útero '
                                                                                                                                                    'involucionando a nivel infraumbilical; herida '
                                                                                                                                                    'quirúrgica o episiorrafia sin signos de infección',
                                                                                                                                                    'herida quirúrgica o episiorrafia sin signos de '
                                                                                                                                                    'infección; útero involucionando, infraumbilical, '
                                                                                                                                                    'y loquios de cantidad y aspecto normales',
                                                                                                                                                    'útero infraumbilical en involución, loquios '
                                                                                                                                                    'normales en cantidad y aspecto; sin signos de '
                                                                                                                                                    'infección en herida quirúrgica o episiorrafia']}
