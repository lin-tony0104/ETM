# python環境:
使用yml獲取

---
# c++環境
- visual studio build tools 2017
- visual c++ build tools(win 10 SDK, 適用於CMake的c++工具, 測試工具的核心功能-建置工具, x86與x64版C++編譯器ATL, 桌上型電腦版的VC++工具組)
---
# 備註:
- 目前已有附上adaptsize.pyd如果要重新編譯才需要下列步驟

 **cd build** </br>
 **cmake -A x64 ..** </br>
 **cmake --build . --config Release** </br>
 到build/Release/  把adaptsize.pyd取出 並使用 </br>

- adaptsize.pyd 是使用pybind將AdaptSize的C語言實作打包成函式庫使用，打包lookup(o_id, o_size), admit(o_id, o_size)並在完成組裝使用。
