from .schemas import CountFileTestResult, RelatedColumnResultsDict
from fastapi import status

def create_test_response(null_cat_idx:list,null_categories:list, nf_cat_idx: list, nf_cat_rows:list,
                         null_mu_idx:list, null_mus:list, nf_mu_idx: list, nf_mu_rows:list):
    model_idx_val_tuples = [(null_cat_idx, null_categories,nf_cat_idx, nf_cat_rows), 
                            (null_mu_idx, null_mus, nf_mu_idx, nf_mu_rows)]
    results = [] #First cat, then mus
    successful_result = True
    for null_idx, null_values, nf_idx, nf_values in model_idx_val_tuples:
        if len(null_values) > 0 | len(nf_values) > 0:
            results.append(RelatedColumnResultsDict(
                status=status.HTTP_400_BAD_REQUEST,
                detail="Algunas filas contienen valores inválidos",
                null_rows=null_values,
                null_idx=null_idx,
                nf_idx=nf_idx,
                nf_rows=nf_values
            ))
            successful_result = False
        else:
            results.append(RelatedColumnResultsDict(
                status=status.HTTP_200_OK,
                detail="Todas las filas se encuentran en un formato correcto",
                null_rows=null_values,
                null_idx=null_idx,
                nf_idx=nf_idx,
                nf_rows=nf_values
            ))
    result = CountFileTestResult(status=status.HTTP_200_OK if successful_result else status.HTTP_400_BAD_REQUEST,
                                categories=results[0], m_units=results[1], products=results[1])
    return result
    