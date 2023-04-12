from ninja import Router

router = Router()


@router.get("/")
def projects(request):
    return []
