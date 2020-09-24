from elasticsearch_dsl import FacetedSearch, TermsFacet


class RecordPageSearch(FacetedSearch):
    """Faceted search for word records
       Replaces earlier haystack search"""
    index = 'language_acts'
    doc_types = ['RecordEntryDocument', ]

    facets = {
        'language': TermsFacet(field='language'),
        'first_letter': TermsFacet(field='first_letter'),
    }
