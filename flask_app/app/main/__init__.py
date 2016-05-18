from flask import Blueprint, url_for


main = Blueprint('main', __name__) 

## Must stay at bottom to avoid circular dependencies,
## as both these modules need to import the 'main' blueprint.
from . import views, errors