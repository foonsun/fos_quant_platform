# A Digital Currency Quant Platform

# QUICK SETUP

* 1、create fos-server.json in conf directory to config the attributes.such as
    ```
    {
	"OSCAR_SHOP_NAME": "BearQuant",
	"EMAIL_HOST": "smtp.qq.com",
	"EMAIL_USE_SSL": true,
	"EMAIL_PORT": 465,
	"EMAIL_HOST_USER": "bearquant@foxmail.com",
	"EMAIL_HOST_PASSWORD": “xxx",
	"EMAIL_SUBJECT_PREFIX": "BEARQUANT",
	"OSCAR_FROM_EMAIL": "bearquant@foxmail.com"
  }
  ```
* 2、docker-compose up -d

* 3、create the database and import the sql.
   docker exec -ti fos_quant_platform_mysql_1 mysql -u root -p root
   create database quant;
   docker exec -i fos_quant_platform_mysql_1 mysql -uroot -proot quant < ./fos_quant_platform_mysql.sql

# Features:
* support binance,huobi,okex,fcoin,bcex,kucoin,bigone,gate,zb,etc.
* support realtime policy running log view.
* support account management and account deposit by eos.

# Doc
  TBD.

## TODO
 * API access of huobi future.
 * market policy.
 
 
## Thanks
  HuoBiDM
 


 
 
  
