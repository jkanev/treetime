import os
import sys

# Add the application bundle directory to PATH so the bundled Graphviz binaries are found.
# PyInstaller sets sys._MEIPASS to the temporary directory where it extracts the bundle.
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    os.environ['PATH'] = bundle_dir + os.pathsep + os.environ.get('PATH', '')
    
    # On Linux, some libraries may look for others in the same directory.
    # We can add the bundle_dir to LD_LIBRARY_PATH if needed.
    # However, PyInstaller's bootloader already handles this to some extent.
    # But for external binaries like 'dot', it might be necessary.
    os.environ['LD_LIBRARY_PATH'] = bundle_dir + os.pathsep + os.environ.get('LD_LIBRARY_PATH', '')

    # Graphviz needs to know where its plugins are. 
    # We bundle them in a 'graphviz' subdirectory within the bundle.
    # We must also point to the 'config6' file, but graphviz expects it in the same 
    # directory as the plugins.
    os.environ['GV_LIB_PATH'] = os.path.join(bundle_dir, 'graphviz')
