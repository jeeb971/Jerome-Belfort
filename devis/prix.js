// ====== PRIX DE L'ESTIMATION — modifiez ici, les totaux se recalculent tout seuls ======
// Prix HT en euros, estimés pour la Guadeloupe (novembre 2026).
const DEVIS = {
  ref: 'EST-2026-011',
  date: '10/11/2026',
  tva: 0.085, // TVA Guadeloupe (taux normal DOM)
  pack: [
    { titre: 'Modules préfabriqués 2,49 × 6 m', unite: 'u', qte: 4, pu: 6900,
      detail: 'Ossature acier galvanisé, panneaux sandwich isolés (murs et plafond), plancher, cloisons, pré-câblage électrique, attentes plomberie. 14,94 m² par module.' },
    { titre: 'Fret maritime jusqu\'au port de Jarry', unite: 'u', qte: 4, pu: 2000,
      detail: 'Transport maritime de chaque module jusqu\'à Pointe-à-Pitre (Jarry), assurance transport comprise.' },
    { titre: 'Dédouanement, frais portuaires et octroi de mer', unite: 'forf.', qte: 1, pu: 3500,
      detail: 'Transitaire, manutention au port, octroi de mer et octroi de mer régional (estimation).' },
    { titre: 'Livraison sur terrain, grutage et assemblage', unite: 'forf.', qte: 1, pu: 3500,
      detail: 'Camion plateau depuis Jarry, camion-grue, mise en place sur fondations, liaison et étanchéité entre les modules.' },
    { titre: 'Menuiseries aluminium (fourniture et pose)', unite: 'forf.', qte: 1, pu: 6900,
      detail: '1 porte d\'entrée alu (1 300 €), 1 baie coulissante 2,40 m (2 000 €), 4 fenêtres alu 1,00 × 1,25 m (4 × 650 €), 2 jalousies alu pour la salle d\'eau et le WC (2 × 500 €).' },
    { titre: 'Toiture', unite: 'm²', qte: 80, pu: 70,
      detail: 'Charpente légère, tôle bac acier laquée, faîtage, rives, gouttières, fixations para-cycloniques. Débords d\'environ 0,8 m pour l\'ombre et la ventilation.' },
  ],
  dalle: [
    { titre: 'OPTION — Dalle béton armé 10,5 × 6,5 m', unite: 'm²', qte: 68, pu: 115,
      detail: 'Fondations (semelles et longrines), hérisson, film polyane, dalle de 12 cm ferraillée, réservations pour l\'eau, l\'électricité et l\'évacuation. Béton livré en toupie.' },
    { titre: 'OPTION — Implantation et préparation du terrain', unite: 'forf.', qte: 1, pu: 1200,
      detail: 'Implantation, décapage de la terre végétale, mise à niveau sur un terrain plat.' },
  ],
};
