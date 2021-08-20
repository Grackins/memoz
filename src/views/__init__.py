from .states import STATE_HOME, STATE_REVIEW_OLD_CARD, STATE_ADD,\
        STATE_REVIEW_NEW_CARD, STATE_STATS
from .home import HomeView
from .old_card_review import OldCardReviewView
from .new_card_review import NewCardReviewView
from .add_card import AddCardView
from .stats import StatsView


view_funcs = {
    STATE_HOME: HomeView.as_view(),
    STATE_REVIEW_OLD_CARD: OldCardReviewView.as_view(),
    STATE_REVIEW_NEW_CARD: NewCardReviewView.as_view(),
    STATE_ADD: AddCardView.as_view(),
    STATE_STATS: StatsView.as_view(),
}
