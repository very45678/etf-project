# scheduler.py
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from price_fetcher import fetch_all_funds
from nav_fetcher import fetch_all_funds_nav
from yield_calculator import calculate_yields_for_all_funds, check_arb_opportunities_for_all_funds
from data_store import insert_error
from data_cleanup import cleanup_old_data

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('scheduler')

class FundDataScheduler:
    """
    基金数据定时任务调度器
    """
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False
        
    def start_price_fetching(self):
        """
        启动价格数据采集任务（每5分钟执行一次）
        """
        try:
            logger.info("开始执行价格数据采集任务...")
            success_count = fetch_all_funds()
            logger.info(f"价格数据采集完成，成功获取 {success_count} 条数据")
            
            # 价格数据采集完成后，自动触发收益率计算
            if success_count > 0:
                self.start_yield_calculation()
                
        except Exception as e:
            error_msg = f"价格数据采集任务失败: {str(e)}"
            logger.error(error_msg)
            insert_error('价格数据采集任务失败', str(e))
    
    def start_nav_fetching(self):
        """
        启动净值数据采集任务（每天执行一次）
        """
        try:
            logger.info("开始执行净值数据采集任务...")
            success_count = fetch_all_funds_nav()
            logger.info(f"净值数据采集完成，成功获取 {success_count} 条数据")
        except Exception as e:
            error_msg = f"净值数据采集任务失败: {str(e)}"
            logger.error(error_msg)
            insert_error('净值数据采集任务失败', str(e))
    
    def start_yield_calculation(self):
        """
        启动收益率计算任务
        """
        try:
            logger.info("开始执行收益率计算任务...")
            success_count = calculate_yields_for_all_funds()
            logger.info(f"收益率计算完成，成功计算 {success_count} 只基金的收益率")
        except Exception as e:
            error_msg = f"收益率计算任务失败: {str(e)}"
            logger.error(error_msg)
            insert_error('收益率计算任务失败', str(e))
    
    def start_arb_check(self):
        """
        启动套利机会检查任务
        """
        try:
            logger.info("开始执行套利机会检查任务...")
            arb_count = check_arb_opportunities_for_all_funds()
            logger.info(f"套利机会检查完成，发现 {arb_count} 只基金存在套利机会")
        except Exception as e:
            error_msg = f"套利机会检查任务失败: {str(e)}"
            logger.error(error_msg)
            insert_error('套利机会检查任务失败', str(e))
    
    def start_data_cleanup(self):
        """
        启动数据清理任务
        """
        try:
            logger.info("开始执行数据清理任务...")
            cleanup_old_data(days=5)
            logger.info("数据清理任务完成")
        except Exception as e:
            error_msg = f"数据清理任务失败: {str(e)}"
            logger.error(error_msg)
            insert_error('数据清理任务失败', str(e))
    
    def start_scheduler(self):
        """
        启动定时任务调度器
        """
        try:
            # 添加价格数据采集任务 - 每5分钟执行一次
            price_trigger = IntervalTrigger(minutes=5)
            self.scheduler.add_job(
                self.start_price_fetching,
                trigger=price_trigger,
                id='price_fetching',
                name='价格数据采集任务',
                replace_existing=True
            )
            
            # 添加净值数据采集任务 - 每天9:30执行（开盘时间）
            nav_trigger = CronTrigger(hour=9, minute=30)
            self.scheduler.add_job(
                self.start_nav_fetching,
                trigger=nav_trigger,
                id='nav_fetching',
                name='净值数据采集任务',
                replace_existing=True
            )
            
            # 添加收益率计算任务 - 每10分钟执行一次（独立任务）
            yield_trigger = IntervalTrigger(minutes=10)
            self.scheduler.add_job(
                self.start_yield_calculation,
                trigger=yield_trigger,
                id='yield_calculation',
                name='收益率计算任务',
                replace_existing=True
            )
            
            # 添加套利机会检查任务 - 每15分钟执行一次
            arb_trigger = IntervalTrigger(minutes=15)
            self.scheduler.add_job(
                self.start_arb_check,
                trigger=arb_trigger,
                id='arb_check',
                name='套利机会检查任务',
                replace_existing=True
            )
            
            # 添加数据清理任务 - 每天凌晨2点执行
            cleanup_trigger = CronTrigger(hour=2, minute=0)
            self.scheduler.add_job(
                self.start_data_cleanup,
                trigger=cleanup_trigger,
                id='data_cleanup',
                name='数据清理任务',
                replace_existing=True
            )
            
            # 启动调度器
            self.scheduler.start()
            self.is_running = True
            logger.info("定时任务调度器已启动")
            logger.info("价格数据采集任务：每5分钟执行一次")
            logger.info("净值数据采集任务：每天9:30执行")
            logger.info("收益率计算任务：每10分钟执行一次")
            logger.info("套利机会检查任务：每15分钟执行一次")
            
        except Exception as e:
            error_msg = f"启动定时任务调度器失败: {str(e)}"
            logger.error(error_msg)
            insert_error('启动定时任务调度器失败', str(e))
    
    def stop_scheduler(self):
        """
        停止定时任务调度器
        """
        try:
            if self.scheduler and self.scheduler.running:
                self.scheduler.shutdown()
                self.is_running = False
                logger.info("定时任务调度器已停止")
        except Exception as e:
            error_msg = f"停止定时任务调度器失败: {str(e)}"
            logger.error(error_msg)
            insert_error('停止定时任务调度器失败', str(e))
    
    def get_scheduler_status(self):
        """
        获取调度器状态
        """
        return {
            'is_running': self.is_running,
            'jobs': [str(job) for job in self.scheduler.get_jobs()] if self.scheduler else []
        }

def main():
    """
    主函数 - 启动定时任务调度器
    """
    scheduler = FundDataScheduler()
    
    try:
        # 启动调度器
        scheduler.start_scheduler()
        
        # 保持程序运行
        logger.info("定时任务调度器正在运行，按 Ctrl+C 停止...")
        while scheduler.is_running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("接收到停止信号，正在停止调度器...")
    except Exception as e:
        logger.error(f"调度器运行异常: {str(e)}")
    finally:
        scheduler.stop_scheduler()
        logger.info("程序已退出")

if __name__ == '__main__':
    main()