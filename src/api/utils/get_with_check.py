from fastapi import HTTPException, status


def get_with_check(id: int, service):
    result = service.get(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Операция не найдена")
    return result
