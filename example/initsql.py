import linksql

link = linksql.C919SQL()
link.root_link('root', 'root')  # 本行修改为自己的 root 账号密码

link.execute("create user c919 identified by 'c919';")
link.execute("grant all privileges on c919db.* to c919@'%';")
link.execute("flush privileges;")
link.execute("use c919db;")

link.execute("""
CREATE TABLE `c919db`.`user_info` (
  `uid` INT NOT NULL,
  `name` VARCHAR(512) NULL,
  `email` VARCHAR(512) NULL,
  `tele` VARCHAR(512) NULL,
  `password` VARCHAR(512) NULL,
  `wechat` VARCHAR(512) NULL,
  `weibo` VARCHAR(512) NULL,
  `ischeck` TINYINT ZEROFILL NULL DEFAULT 0,
  `isfrozen` TINYINT ZEROFILL NULL DEFAULT 0,
  PRIMARY KEY (`uid`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `tele_UNIQUE` (`tele` ASC) VISIBLE,
  UNIQUE INDEX `wechat_UNIQUE` (`wechat` ASC) VISIBLE);
""")

link.execute("""
DROP TRIGGER IF EXISTS `c919db`.`user_info_BEFORE_INSERT`;
""")

link.execute("""
USE `c919db`;
""")

link.execute("""
CREATE DEFINER = CURRENT_USER TRIGGER `c919db`.`user_info_BEFORE_INSERT` BEFORE INSERT ON `user_info` FOR EACH ROW
BEGIN
    declare randid int;
    label:
    while true do
        set randid = (select floor(1 + rand() * 9999));
        if randid not in (select uid from user_info) then
            leave label;
        end if;
    end while;
    set new.uid = randid;
END
""")

link.end_link()