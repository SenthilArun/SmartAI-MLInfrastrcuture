import streamlit as st
import psutil
from datetime import datetime

def get_cpu_memory_stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    return cpu_percent, memory_percent

def get_gpu_stats():
    gpu_stats = []
    
    try:
        import gpustat
        gpus = gpustat.new_query()
        for gpu in gpus.gpus:
            gpu_stats.append({
                'id': gpu.uuid,
                'name': gpu.name,
                'memory_total': gpu.memory_total,
                'memory_used': gpu.memory_used,
                'memory_free': gpu.memory_free,
                'memory_utilization': round((gpu.memory_used / gpu.memory_total) * 100, 1),
                'gpu_utilization': gpu.utilization,
                'temperature': gpu.temperature,
                'power_draw': getattr(gpu, 'power_draw', None)
            })
    except ImportError:
        st.warning("GPU monitoring requires the 'gpustat' library.")
        with st.expander("Installation Instructions"):
            st.code("pip install gpustat", language="bash")
            st.markdown("**Note:** You may need to restart your application after installing.")
    except Exception as e:
        st.error(f"Error getting GPU stats: {e}")
    
    return gpu_stats

def display_gpu_info(gpu_stats):
    if not gpu_stats:
        return
    
    for gpu in gpu_stats:
        st.markdown(f"### 🎮 {gpu['name']} ")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            gpu_util = gpu.get('gpu_utilization', 'N/A')
            if isinstance(gpu_util, (int, float)):
                st.metric(label="GPU Utilization", value=f"{gpu_util}%")
                st.progress(float(gpu_util) / 100.0)
            else:
                st.metric(label="GPU Utilization", value=gpu_util)
        
        with col2:
            mem_util = gpu.get('memory_utilization', 'N/A')
            if isinstance(mem_util, (int, float)):
                mem_usage = f"{gpu['memory_used']} MB / {gpu['memory_total']} MB"
                st.metric(label="Memory Usage", value=f"{mem_util}%")
                st.progress(float(mem_util) / 100.0)
                st.caption(mem_usage)
            else:
                st.metric(label="Memory Usage", value=mem_util)
        
        with col3:
            temp = gpu.get('temperature', 'N/A')
            power = gpu.get('power_draw', 'N/A')
            
            if isinstance(temp, (int, float)):
                temp_color = "🟢" if temp < 70 else "🟡" if temp < 85 else "🔴"
                st.metric(label="Temperature", value=f"{temp}°C", delta=temp_color)
            else:
                st.metric(label="Temperature", value=temp)
            
            if isinstance(power, (int, float)) and power is not None:
                st.metric(label="Power Draw", value=f"{power}W")
            else:
                st.metric(label="Power Draw", value="N/A")

def main():
    st.title("🖥️ System Monitoring Dashboard")

    auto_refresh = st.checkbox("Auto-refresh (3s)", value=True)
    
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    
    current_time = datetime.now()
    time_elapsed = (current_time - st.session_state.last_refresh).total_seconds()
    
    if auto_refresh and time_elapsed >= 3:
        st.session_state.last_refresh = current_time
        st.rerun()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💻 CPU & Memory")
        
        try:
            cpu_percent, memory_percent = get_cpu_memory_stats()
            
            st.metric(label="CPU Usage", value=f"{cpu_percent}%")
            st.progress(cpu_percent / 100.0)
            
            st.metric(label="Memory Usage", value=f"{memory_percent}%")
            st.progress(memory_percent / 100.0)
        
        except Exception as e:
            st.error(f"Error getting CPU/Memory stats: {e}")
    
    with col2:
        st.subheader("🎮 GPU Information")
        gpu_stats = get_gpu_stats()
        display_gpu_info(gpu_stats)

    st.divider()

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button('🔄 Refresh Now', type="primary"):
            st.rerun()
    
    with col2:
        if st.button('📊 System Info'):
            with st.expander("System Information", expanded=True):
                import platform
                st.write(f"**OS:** {platform.system()} {platform.release()}")
                st.write(f"**Python:** {platform.python_version()}")
                st.write(f"**Processor:** {platform.processor()}")
    
    with col3:
        st.caption(f"Last updated: {st.session_state.last_refresh.strftime('%H:%M:%S')}")

if __name__ == '__main__':
    try:
        st.set_page_config(
            page_title="System Monitor",
            page_icon="🖥️",
            layout="wide"
        )
        main()
    except Exception as e:
        print("System Monitor")
        print("=" * 50)
        print(f"Error: {e}")
        print("To run the web interface, use: streamlit run <script_name>")