import requests, json, logging, datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from django.conf import settings
from oscar.apps.customer.models import AbstractDepositRecords
from oscar_accounts.models import Account, AccountType

log_sync_orders = logging.getLogger('sync_orders_log')
class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        url = 'http://eos.greymass.com/v1/history/get_actions'
        payload = {"account_name": settings.EOS_WALLET_ADDRESS ,"pos":-1,"offset":-50}
        response = requests.post(url, data=json.dumps(payload))
        result = json.loads(response.content)
        actions = result['actions']
        for action in actions:
            if 'action_trace' in action and 'receipt' in action['action_trace'] and 'act' in action['action_trace']:
                if action['action_trace']['act']['account'] == 'eosio.token' and action['action_trace']['act']['name'] == 'transfer':
                    result = action['action_trace']['act']['data']
                    if result['to'] == settings.EOS_WALLET_ADDRESS:
                        payaccount = result['from']
                        amount = float(result['quantity'].split()[0])
                        memo = result['memo']
                        txid = action['action_trace']['trx_id']
                        block_num  = action['action_trace']['block_num']
                        native_time = datetime.datetime.strptime(action['action_trace']['block_time'], '%Y-%m-%dT%H:%M:%S.%f')
                        block_time = make_aware(native_time + datetime.timedelta(hours=8))
                        record = AbstractDepositRecords.objects.filter(txid=txid)
                        if record:
                            continue
                        tx_url = 'https://eos.greymass.com/v1/history/get_transaction'
                        payload = {"block_num_hint": block_num, "id": txid}
                        rsp = requests.post(tx_url, data=json.dumps(payload))
                        result = json.loads(rsp.content)
                        if result['trx']['receipt']['status'] == 'executed':
                            url = 'https://api.binance.com/api/v1/klines?interval=1m&limit=1&symbol=EOSUSDT'
                            rsp = requests.get(url)
                            result = json.loads(rsp.content)
                            usdt_close_price = float(result[0][4])
                            url = 'https://api-pub.bitfinex.com/v2/candles/trade:1m:tUSTUSD/last'
                            rsp = requests.get(url)
                            result = json.loads(rsp.content)
                            usdt_usd_price = result[4]
                            url = 'http://data.fixer.io/api/latest?access_key=69e59b50bd4257b4219b545eb03b5be8&format=1&symbols=usd,cny'
                            rsp = requests.get(url)
                            result = json.loads(rsp.content)
                            usd_rmb_price = result['rates']['CNY'] / result['rates']['USD']
                            rmb_price = usdt_close_price * usd_rmb_price * usdt_usd_price
                            AbstractDepositRecords.objects.get_or_create(txid = txid,defaults={
                                                                                    'payaccount': payaccount,
                                                                                    'memo': memo,
                                                                                    'amount': amount,
                                                                                    'txid': txid,
                                                                                    'source': 'EOS',
                                                                                    'block_time': block_time,
                                                                                    'price': rmb_price,
                                                                                    })
                            
                            tag = memo.strip()
                            try:
                                account = Account.objects.get(code=tag)
                            except Account.DoesNotExist:
                                log_sync_orders.info('deposit tag DoesNotExist txid: %s need to check manually' % (txid))
                                continue 
                            deposit_amount = rmb_price*amount
                            account.balance = account.balance + deposit_amount
                            account.save()
                            
                            
                               
                            
                            
                              
                            

                        
                         
        