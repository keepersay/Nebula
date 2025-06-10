from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from init.database import Base

class Server(Base):
    """
    服务器信息模型类
    用于存储和管理服务器的基本信息、网络信息、硬件信息等
    """
    __tablename__ = "server"  # 数据库表名


    # 基本信息
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    service_tag: Mapped[str] = mapped_column(String(100), default="")  # 设备序列号
    name: Mapped[str] = mapped_column(String(100), default="")  # 服务器名
    agent_name: Mapped[str] = mapped_column(String(100), default="")  # Agent抓取主机名
    
    # IP信息
    primary_ip: Mapped[str] = mapped_column(String(100), default="")  # 主IP
    agent_ip: Mapped[str] = mapped_column(String(100), default="")  # Agent抓取ip
    other_ip: Mapped[str] = mapped_column(String(100), default="")  # 其他ip地址
    port: Mapped[str] = mapped_column(String(100), default="")  # docker端口

    # 管理卡信息
    manage_card_ip: Mapped[str] = mapped_column(String(50), default="")  # 管理卡IP地址
    manage_card_mac: Mapped[str] = mapped_column(String(50), default="")  # 管理卡MAC地址
    manage_card_version: Mapped[str] = mapped_column(String(256), default="")  # 管理卡固件版本

    # 系统信息
    bios_version: Mapped[str] = mapped_column(String(256), default="")  # BIOS版本号
    raid_fw_version: Mapped[str] = mapped_column(String(256), default="")  # RAID卡固件版本
    agent_version: Mapped[str] = mapped_column(String(200), default="")  # Agent版本
    agent_kernel: Mapped[str] = mapped_column(String(200), default="")  # agent内核

    # 状态信息
    use_status: Mapped[str] = mapped_column(String(20), default='ready')  # 使用状态（未分配、准备中、上线、下线）
    service_level: Mapped[int] = mapped_column(Integer, default=0)  # 服务级别
    is_installing: Mapped[int] = mapped_column(Integer, default=0)  # 是否正在安装（0-否，1-是）
    install_status: Mapped[str] = mapped_column(String(20), default='uninstall')  # 装机状态
    lock_status: Mapped[str] = mapped_column(String(20), default='unlocked')  # 锁状态

    # 时间信息
    due_date: Mapped[datetime] = mapped_column(DateTime, default=datetime(1970, 1, 1))  # 服务器到期日期
    using_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # 启用时间

    # 虚拟机信息
    is_vm: Mapped[int] = mapped_column(Integer, default=0)  # 是否虚拟机
    real_server_id: Mapped[int] = mapped_column(BigInteger, default=0)  # 宿主机id
    vm_type: Mapped[str] = mapped_column(String(20), default='undefined')  # 虚拟机类型
    vm_network_type: Mapped[str] = mapped_column(String(20), default='undefined')  # 虚拟机网络类型
    instance_name: Mapped[str] = mapped_column(String(100), default="")  # 实例名称

    # 硬件信息
    cpu_amount: Mapped[int] = mapped_column(Integer, default=0)  # CPU数量
    cpu_cores: Mapped[int] = mapped_column(Integer, default=0)  # CPU物理核总数
    cpu_kernel_number: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00)  # CPU线程总数
    ram_amount: Mapped[int] = mapped_column(Integer, default=0)  # 内存数量
    ram_size: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00)  # 内存大小,单位G
    nic_amount: Mapped[int] = mapped_column(Integer, default=0)  # 网卡数量
    storage_amount: Mapped[int] = mapped_column(Integer, default=0)  # 硬盘数量
    storage_info: Mapped[str] = mapped_column(String(200), default="")  # 存储配置
    filesystem_disk_space: Mapped[int] = mapped_column(Integer, default=0)  # 系统磁盘空间

    # 关联ID
    device_id: Mapped[int] = mapped_column(BigInteger, default=0)  # 设备ID
    group_id: Mapped[int] = mapped_column(BigInteger, default=0)  # 分组ID
    agent_os_id: Mapped[int] = mapped_column(BigInteger, default=0)  # agent采集的操作系统ID
    template_id: Mapped[int] = mapped_column(BigInteger, default=0)  # 装机模板ID
    image_id: Mapped[int] = mapped_column(BigInteger, default=0)  # 镜像ID
    network_segment_id: Mapped[int] = mapped_column(BigInteger)  # 网段ID

    # 其他信息
    owner: Mapped[str] = mapped_column(String(20), default="")  # 服务器使用人
    label: Mapped[str] = mapped_column(String(100), default="")  # 服务器归属
    description: Mapped[str] = mapped_column(Text)  # 描述

    # 审计信息
    created_by: Mapped[str] = mapped_column(String(20), default="")  # 创建人
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # 创建时间
    last_modified_by: Mapped[str] = mapped_column(String(20), default="")  # 最后修改人
    last_modified_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # 最后修改时间
    is_valid: Mapped[bool] = mapped_column(Boolean, default=True)  # 是否有效

    def __repr__(self):
        return f"<Server(id={self.id}, service_tag={self.service_tag})>"
    