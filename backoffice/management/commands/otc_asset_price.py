import logging

from django.core.management.base import BaseCommand
from common.helpers import d0, dec, sleep
from exchange.models import Symbol, ExchangeSymbolShip
from backoffice.models import OtcAssetPrice
from exchange.controllers import get_history_orderbook


class Command(BaseCommand):
    def handle(self, *args, **options):
        exchange_symbol_list = ExchangeSymbolShip.objects.all()
        for exchange_symbol in exchange_symbol_list:
            order_book = get_history_orderbook(
                exchange_symbol.exchange.name,
                exchange_symbol.symbol.name
            )
            sell_price = order_book.bids[0].price
            buy_price = order_book.asks[0].price
            avg_price = (sell_price + buy_price) / 2
            usd_cny_price = "6.98"
            OtcAssetPrice.objects.update_or_create(
                asset=exchange_symbol.symbol.quote_asset,
                defaults={
                    "usd_price": dec(avg_price),
                    "cny_price": avg_price * dec(usd_cny_price)
                }
            )
