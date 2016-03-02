import sae.const

SAE_MYSQL_DB = sae.const.MYSQL_DB      # 数据库名
SAE_MYSQL_USER = sae.const.MYSQL_USER    # 用户名
SAE_MYSQL_PASS = sae.const.MYSQL_PASS    # 密码
SAE_MYSQL_HOST_M = sae.const.MYSQL_HOST    # 主库域名（可读写）
SAE_MYSQL_PORT = sae.const.MYSQL_PORT    # 端口，类型为<type 'str'>，请根据框架要求自行转换为int
#sae.const.MYSQL_HOST_S  # 从库域名（只读）