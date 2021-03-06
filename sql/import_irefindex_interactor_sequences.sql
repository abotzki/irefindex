-- Combine the specific interactor details with the identifier sequence details.

-- Copyright (C) 2011, 2012 Ian Donaldson <ian.donaldson@biotek.uio.no>
-- Original author: Paul Boddie <paul.boddie@biotek.uio.no>
--
-- This program is free software; you can redistribute it and/or modify it under
-- the terms of the GNU General Public License as published by the Free Software
-- Foundation; either version 3 of the License, or (at your option) any later
-- version.
--
-- This program is distributed in the hope that it will be useful, but WITHOUT ANY
-- WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
-- PARTICULAR PURPOSE.  See the GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License along
-- with this program.  If not, see <http://www.gnu.org/licenses/>.

begin;

insert into xml_xref_interactor_sequences
    select I.source, I.filename, I.entry, I.interactorid, reftype, reftypelabel,
        I.dblabel, I.refvalue, I.originaldblabel, I.originalrefvalue,
        S.finaldblabel, S.finalrefvalue, missing,
        taxid, sequence, sequencelink, reftaxid, refsequence
    from xml_xref_interactors as I
    left outer join xml_xref_sequences as S
        on (I.dblabel, I.refvalue) = (S.dblabel, S.refvalue)

    -- Filter out non-proteins.

    left outer join xml_xref_interactor_types as T
        on (I.source, I.filename, I.entry, I.interactorid)
         = (T.source, T.filename, T.entry, T.interactorid)

    -- No type information is assumed to mean that interactors are only ever
    -- proteins.

    where T.refvalue is null
        or T.refvalue = 'MI:0326';

create index xml_xref_interactor_sequences_index on xml_xref_interactor_sequences(source, filename, entry, interactorid);
analyze xml_xref_interactor_sequences;

commit;
