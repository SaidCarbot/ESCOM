% Rule-based reasoning
% Este sistema experto implementa

:- dynamic si/1, no/1.
% de que solo tiene un argumento
% es necesario que el dynamic para que los predicados puedan resivir si o no 
% tiempo de ejecución

%1-Menú
main :-
    repeat,
    nl, write('Sistema experto en tipos de neuronas'), nl,
    nl, write('Menú'), nl,
    nl, write('1 Consultar el tipo de neurona'), nl,
    nl, write('2 Salir'), nl,
    nl, write('Teclea tu opción: '), nl,
    read(Opcion), nl,
    (
        (Opcion = 1, motorLogico, fail);
        Opcion = 2, !
    ).


%2-MotorLogico
motorLogico :-
    borraResp,
    (
        deducir(Objeto, _) ->
        (
            nl, write('Deduzco que el tipo de neurona es: '), write(Objeto),
            nl, write('Tal que: '), findall(X, si(X), L), writeln(L)
        );
        nl, write('No puedo reconocer una neurona con la descripción dada')
    ).

%3-Lógica
satisface(Atributo,_) :-
(si(Atributo)  -> true ;
%if   si(Atributo) then true
    (no(Atributo) -> fail ;		   %else if no(Atributo) then fail
                    pregunta(Atributo))). %else pregunta(Atributo)

%4-Interacción
pregunta(A) :-
    write('¿Tu neurona '),
    write(A),
    write('? (s/si para sí, cualquier otra para no) '),
    read(Resp),
    nl,
    (
        (Resp = s ; Resp = si ; Resp = 's' ; Resp = 'si')
        -> assert(si(A))
        ; assert(no(A)), fail
    ).


borraResp :-
    retractall(si(_)),
    retractall(no(_)).

%5-BaseDeConocimientos
deducir(sensorial, X) :- sensor(X).
deducir(interneurona, X) :- interneurona(X).
deducir(motora, X) :- motora(X).
deducir(inhibidora, X) :- inhibidora(X).
deducir(excitadora, X) :- excitadora(X).

sensor(X) :-
    satisface(detecta_estimulos,X),
    satisface(es_unipolar_o_bipolar,X),
    satisface(envia_a_interneuronas_o_medula,X),
    satisface(responde_a_luz,X).

interneurona(X) :-
    satisface(procesa_entre_sensoriales_y_motoras,X),
    satisface(es_multipolar,X),
    satisface(modula_circuitos_locales,X),
    satisface(esta_en_corteza_o_cerebelo,X).

motora(X) :-
    satisface(controla_musculos_o_glandulas,X),
    satisface(es_multipolar_medula_o_tronco,X),
    satisface(recibe_de_interneuronas_o_corteza,X),
    satisface(ejemplo_cuerno_ventral,X).

inhibidora(X) :-
    satisface(disminuye_actividad_con_gaba,X),
    satisface(tiene_proyecciones_cortas,X),
    satisface(sincroniza_redes,X),
    satisface(ejemplo_canasta_hipocampo,X).

excitadora(X) :-
    satisface(aumenta_actividad_con_glutamato,X),
    satisface(tiene_proyecciones_largas,X),
    satisface(forman_vias_principales,X),
    satisface(ejemplo_piramidal_corteza,X).

%References
/*
[1]E. R. Kandel, J. H. Schwartz, and T. M. Jessell, Principles of Neural Science, 4th ed. New York, NY, USA: McGraw-Hill, 2000.
[2]M. F. Bear, B. W. Connors, and M. A. Paradiso, Neuroscience: Exploring the Brain, 4th ed. Philadelphia, PA, USA: Wolters Kluwer, 2016.
[3]G. M. Shepherd, The Synaptic Organization of the Brain, 5th ed. Oxford, U.K.: Oxford Univ. Press, 2004.
[4]Z. J. Huang and A. Paul, "The diversity of GABAergic neurons and neural communication elements," Nature Rev. Neurosci., vol. 20, no. 9, pp. 563–572, Sep. 2019.
[5]G. A. Ascoli et al., "Petilla terminology: Nomenclature of features of GABAergic interneurons of the cerebral cortex," Nature Rev. Neurosci., vol. 9, no. 7, pp. 557–568, Jul. 2008.*/

% By Said Carbot & Aaron Ugalde
% MEX-IPN-ESCOM-IA-2025/2-mayo
